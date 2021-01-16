import tensorflow_hub as hub
import tensorflow_text  # 임포트하지 않으면 오류 발생
from .utils import cos_sim, dedup


class Encoder:
    def __init__(self):
        """
        Sentence Encoder
        """
        self.model = self.load_model()
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

    def compare(self, org: str, others: list) -> list:
        # 원래 문장(org)을 others와 비교하여 각각의 유사도를 구하여 반환
        # ex) f('안녕하세요 저는 조준희입니다', ['안녕', '저', '조준희']) -> [0.698, 0.501, 0.821]
        embed = self.model([org] + others)  # 임베딩
        org_v, others_v = embed[0], embed[1:]

        # 유사도 구하기
        r = [self.criterion(org_v, v) for idx, v in enumerate(others_v)]
        return r
