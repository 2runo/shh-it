import torch
import numpy as np
import re
from transformers import BertTokenizer, BertForMaskedLM

from .utils import index, softmax
from .encoder import Encoder


class Purifier:
    def __init__(self, curse_detector, device=None):
        """
        욕설 문장 순화
        """
        self.device = self.get_device(device)
        self.tokenizer = BertTokenizer.from_pretrained("beomi/kcbert-large")
        self.model = BertForMaskedLM.from_pretrained("beomi/kcbert-large").to(self.device)

        self.encoder = Encoder()  # sentence encoder
        self.curse_detector = curse_detector

    @staticmethod
    def get_device(device):
        if not device:
            if torch.cuda.is_available():
                device = torch.device("cuda")
            else:
                device = torch.device("cpu")
        return device

    @staticmethod
    def masking(text, mask="[MASK]"):
        # *별표로 감싸져 있는 단어 replace
        # ex) f("안녕하세요 *저는* 조준희입니다") -> "안녕하세요 [MASK] 조준희입니다"
        return text.replace(re.findall(r'\*\w+\*', text)[0], mask)

    @staticmethod
    def get_org_text(text):
        # *별표로 감싸져 있는 단어에서 별표 제거
        w = re.findall(r'\*\w+\*', text)[0]
        return text.replace(w, w[1:-1])

    def encode(self, text):
        # text -> tokens
        return torch.LongTensor(
            self.tokenizer.encode(text, return_tensors="pt")
        ).to(self.device)

    def decode(self, tokens):
        # tokens -> text
        return self.tokenizer.decode(tokens)

    def predict(self, tokens: torch.LongTensor, i: int):
        # model predict 후 i번째 토큰의 distribution 반환
        out = self.model(tokens)
        logits = out.logits.cpu().detach().numpy()
        logits = logits[:, 1:-1]  # [CLS], [SEP] 토큰 제거
        return logits[0][i]

    def unmask(self, text, top_n=50):
        # unmask ([MASK] 부분에 들어갈 단어 후보 top_n개 반환)
        # ex) f("안녕하세요 저는 조준희입니다 [MASK]") -> [(0.6662801, '.'), (0.0961391, '!'), ...]
        tokens: torch.LongTensor = self.encode(text)
        mask_idx: int = index(tokens, self.tokenizer.mask_token_id)  # [MASK] 위치
        confidence = self.predict(tokens, mask_idx)
        confidence: np.ndarray = softmax(confidence)
        return sorted(zip(confidence, self.tokenizer.get_vocab()), reverse=True)[:top_n]

    def purify(self, text, masked):
        # 욕설 문장 순화 (순화할 단어는 *로 감싸져 있어야 함)
        # ex) "이런 *짐승*같은 놈"
        # ex) f("이런 *짐승*같은 새끼", "이런 *짐승*같은 §")
        org_text = self.get_org_text(text)  # remove '*'
        masked_text = self.masking(text)  # replace [MASK]
        words = self.unmask(masked_text)
        words.append((np.average([i[0] for i in words[:len(words)//2]]), ''))

        # 욕설 단어 필터링
        c = [self.masking(masked, word[1].replace('##', '')).replace('§', '') for word in words]
        a = self.curse_detector.predict(c)[0]
        words = np.array(words)[a<=0.5]
        if len(words) == 0:
            # 후보가 모두 욕이라면?
            return [(1.0, '*')]

        others = [masked_text.replace("[MASK]", word[1].replace('##', '')) for word in words]

        sim = np.array(self.encoder.compare(org_text, others)) ** 3
        sim = softmax(sim)

        final_sim = np.array(sim) + words[:,0].astype('float32')
        return sorted([(final_sim[i], j[1]) for i, j in enumerate(words)], reverse=True)

    def __call__(self, text):
        org_idx = []
        tokens = self.curse_detector.komoran.morphs(text)

        out, att = self.curse_detector.predict_tokens([tokens])
        out, att = out[0], att[0]

        if out < 0.5:
            # 욕설이 아니라면?
            return text

        while out >= 0.5:
            idx = np.argmax(att)
            if tokens[idx] == '':
                # mask를 보고 욕이라 착각하면?
                break
            org_idx.append((idx, tokens[idx]))
            tokens[idx] = ''  # mask

            out, att = self.curse_detector.predict_tokens([tokens])
            out, att = out[0], att[0]

        purify_result = []
        for idx, curse_word in org_idx:
            masked_text = text
            for _, curse_word2 in org_idx:
                if curse_word != curse_word2:
                    masked_text = masked_text.replace(curse_word2, '§', 1)
            _text = text.replace(curse_word, '*' + curse_word + '*', 1)
            masked_text = masked_text.replace(curse_word, '*' + curse_word + '*', 1)

            out = self.purify(_text, masked_text)
            purify_result.append((curse_word, out[0][1]))

        result = text
        for (a, b) in purify_result:
            if b[:2] == '##':
                b = b[2:]
            result = result.replace(a, b, 1)
            result = result.replace("OOO야", "사람아")
            result = result.replace("OOO가", "사람이")
            result = result.replace("OOO는", "사람은")
            result = result.replace("OOO이가", "사람이")
            result = result.replace("OOO", "사람")
        return result
