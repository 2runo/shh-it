from curse_detection import CurseDetector

curse = CurseDetector()
print(curse.predict(['안녕하세요 저는 조준희입니다', '원시인 같은 새기']))
while True:
    text = input(':')
    print(curse.predict(text))
