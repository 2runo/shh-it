from konlpy.tag import Okt
from tensorflow.keras import Model

from .model import ClassificationModel


class CurseDetector:
    def __init__(self, weights_path="curse_detection/weights-short.h5"):
        self.komoran = Okt()
        model_parent = ClassificationModel()
        self.model = model_parent.build_model()
        self.att_model = Model(inputs=[self.model.input], outputs=self.model.layers[10].output)
        self.embedding = model_parent.embedding

        self.model.load_weights(weights_path)

    def predict(self, texts):
        is_str = False
        if isinstance(texts, str):
            texts = [texts]
            is_str = True

        tokens = []
        for text in texts:
            try:
                tokens.append(self.komoran.morphs(text))
            except UnicodeDecodeError:
                tokens.append(['*'])
        out, att = self.predict_tokens(tokens)
        if is_str:
            return out[0], att[0]
        else:
            return out, att

    def predict_tokens(self, tokens):
        inp, mask = self.embedding(tokens)
        out = self.model.predict((inp, mask)).squeeze(1)  # 욕설일 확률
        att = self.att_model.predict((inp, mask))[1].squeeze(2)  # attention score
        return out, att


if __name__ == "__main__":
    curse = CurseDetector()
    print(curse.predict(['안녕하세요 저는 조준희입니다', '아니 씨발', '원시인 같은 새기']))
    while True:
        inp = input(':')
        print(curse.predict(inp))
