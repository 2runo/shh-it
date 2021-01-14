from konlpy.tag import Komoran


class Tagger:
    def __init__(self, mode: str = "nouns"):
        """
        konlpy pos tagger
        """
        self.tagger = Komoran()
        self.mode = mode  # nouns, morphs

    def __call__(self, *args, **kwargs) -> list:
        if self.mode == "nouns":
            return self.tagger.nouns(*args, **kwargs)
        elif self.mode == "morphs":
            return self.tagger.morphs(*args, **kwargs)


if __name__ == "__main__":
    tag = Tagger()
    print(tag("완전한 테스트입니다"))
