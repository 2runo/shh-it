import numpy as np

from purify import Purifier
from curse_detection import CurseDetector

if __name__ == "__main__":
    curse = CurseDetector()
    p = Purifier(curse)

    while True:
        inp = input(':')

        print(p(inp))
