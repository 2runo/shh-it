"""
data loader
"""
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from konlpy.tag import Komoran


class DataLoader:
    def __init__(self, path="curse_detection/dataset/long.txt", one_hot=False, max_len=30):
        self.path = path
        self.one_hot = one_hot  # True: [0~1, 0~1]  False: 0~1
        self.max_len = max_len

        self.komoran = Komoran()

    def get_data(self):
        x, y = self.load()
        x_train, x_test, y_train, y_test = self.split(x, y)
        return x_train, x_test, y_train, y_test

    @staticmethod
    def one_hot_encoding(y):
        # 원 핫 인코딩
        return np.eye(2)[y.astype("int8")]

    def load(self):
        with open(self.path, 'r', encoding='utf8') as f:
            data = f.read()
        data = data.split('\n')

        x, y = [], []
        for line in data:
            try:
                tmp = self.tokenize('|'.join(line.split('|')[:-1]))
            except UnicodeDecodeError:
                continue
            if len(tmp) > self.max_len:
                continue
            x.append(tmp)
            y.append(line.split('|')[-1].replace('"', ''))
        y = np.array(y, dtype=np.float32)
        if self.one_hot:
            y = self.one_hot_encoding(y)
        return x, y

    @staticmethod
    def split(x, y):
        # train test split
        x, y = shuffle(x, y)
        return train_test_split(x, y, test_size=0.1)

    def tokenize(self, text):
        return self.komoran.morphs(text)
