from .encoder import Encoder


class KeywordExtractor:
    def __init__(self):
        """
        keyword extractor
        """
        self.enc = Encoder()

    def __call__(self, *args, **kwargs):
        return self.enc(*args, **kwargs)
