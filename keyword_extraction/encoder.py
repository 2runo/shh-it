import tensorflow_hub as hub
import tensorflow_text  # 임포트하지 않으면 오류 발생
from .utils import cos_sim, dedup
from .tagger import Tagger


class Encoder:
    def __init__(self):
        """
        Sentence Encoder
        """
        self.model = self.load_model()
        self.tag = Tagger()  # 품사 태거
        self.criterion = cos_sim  # 유사도 판단 함수
        self.stopwords = self.load_stopwords()  # 불용어

    @staticmethod
    def load_model():
        return hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

    @staticmethod
    def load_stopwords():
        with open("keyword_extraction/assets/stopwords.txt", 'r', encoding='utf8') as f:
            raw = f.read()
        return raw.split('\n')

    def remove_stopwords(self, text: list) -> list:
        # 불용어 제거
        return [word for word in text if word.replace(' ', '') not in self.stopwords]

    def compare(self, org: str, words: list) -> list:
        # 원래 문장(org)을 words와 비교하여 각각의 유사도를 구하여 반환
        # ex) f('안녕하세요 저는 조준희입니다', ['안녕', '저', '조준희']) -> [0.698, 0.501, 0.821]
        embed = self.model([org] + words)  # 임베딩
        org_v, words_v = embed[0], embed[1:]

        # 유사도 구하기
        r = [self.criterion(org_v, v) for idx, v in enumerate(words_v)]
        return r

    def analyze(self, sentence: str, top_n=3) -> tuple:
        # sentence : 키워드 추출 대상
        # ex) f('안녕하세요 저는 조준희입니다') -> ['조준희']
        if not sentence.replace(' ', ''):  # 키워드 추출할 문장이 비었다면?
            return None

        words = self.tag(sentence)  # 토크나이징 (명사만 추출)
        words = list(set(words))  # 중복 제거 (연산 줄이기 위해)
        words = self.remove_stopwords(words)  # 불용어 제거
        if not words:  # 키워드 후보가 없으면?
            return None

        # 유사도 비교
        sim = self.compare(sentence, words)
        words = dedup(sorted(words, key=lambda x: sim[words.index(x)], reverse=True))  # 키워드 확률 순 정렬
        return words[:top_n]

    def __call__(self, word: str) -> tuple:
        return self.analyze(word)
