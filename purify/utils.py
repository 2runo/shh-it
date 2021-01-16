import numpy as np


def index(l, find):
    # l.index(find)와 동일
    l = l[0][1:-1]
    for i, e in enumerate(l):
        if e == find:
            return i


def softmax(a):
    exp_a = np.exp(a-np.max(a))
    return exp_a / np.sum(exp_a)


def cos_sim(a: np.ndarray, b: np.ndarray) -> np.float32:
    # cosine similarity
    return np.dot(a, b) / (np.linalg.norm(a)*np.linalg.norm(b))


def dedup(seq):
    # 중복 제거
    # ordered list(set(seq))
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
