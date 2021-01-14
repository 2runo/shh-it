import numpy as np


def cos_sim(a: np.ndarray, b: np.ndarray) -> np.float32:
    # cosine similarity
    return np.dot(a, b) / (np.linalg.norm(a)*np.linalg.norm(b))


def dedup(seq):
    # 중복 제거
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

