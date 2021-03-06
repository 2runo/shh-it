from keyword_extraction import KeywordExtractor


if __name__ == "__main__":
    key = KeywordExtractor()
    print(key("출처 https://wikidocs.net/22530"
              "한국어에서 불용어를 제거하는 방법으로는 간단하게는 이 토큰화 후에 조사, 접속사 등을 제거하는 방법이 있습니다. "
              "하지만 불용어를 제거하려고 하다보면 조사나 접속사와 같은 단어들뿐만 아니라 명사, "
              "형용사와 같은 단어들 중에서 불용어로서 제거하고 싶은 단어들이 생기기도 합니다. "
              "결국에는 사용자가 직접 불용어 사전을 만들게 되는 경우가 많습니다. "
              "이번에는 직접 불용어를 정의해보고, 주어진 문장으로부터 직접 정의한 불용어 사전을 참고로 불용어를 제거해보겠습니다."))
