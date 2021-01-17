# python 3.7

from purify import Purifier
from curse_detection import CurseDetector
from download_youtube_subtitle.main import main as download_subtitle

import asyncio
import websockets
import ssl

curse = CurseDetector()
p = Purifier(curse)


class wsServer():
    def __init__(self, host, port, certfile=None, keyfile=None):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile

        if certfile != None:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(self.certfile, self.keyfile)
        else:
            self.ssl_context = None
        self.server = websockets.serve(self.ws_handler, self.host, self.port, ssl=self.ssl_context)

        print('run server')
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    async def predict(self, subtitle):
        r = []
        for sub in subtitle:
            tmp = sub.copy()
            text = sub['text'].replace('\n', ' ')
            tmp['text'] = text
            text = text.replace('새X', '새끼')
            text = text.replace('씨X', '씨발')
            text = text.replace('X들', '새끼들')
            text = text.replace('X 들', '새끼들')
            text = text.replace('시X', '시발')
            text = text.replace('X발', '씨발')
            text = text.replace('X키', '새끼')
            text = text.replace('존X', '존나')
            text = text.replace('X나', '존나')
            text = text.replace('졸라', '존나')
            text = text.replace('병X', '병신')
            text = text.replace('븅X', '병신')
            text = text.replace('X신', '병신')
            text = text.replace('X같', '좆같')
            text = text.replace('X 같', '좆같')
            text = text.replace('지X', '지랄')
            text = text.replace('X랄', '지랄')
            text = text.replace('X밥', '좆밥')
            text = text.replace('X되', '좆되')
            text = text.replace('X돼', '좆돼')
            text = text.replace('X 되', '좆되')
            text = text.replace('X 돼', '좆돼')
            text = text.replace('X까', '좆까')
            text = text.replace('쥰X', '존나')
            text = text.replace('X내', '존나')
            out = p(text)
            if out == text:
                # 욕설 아닐 때
                tmp['curse'] = 0
            else:
                # 욕설일 때
                tmp['curse'] = 1
                tmp['purified'] = out.replace('\n', '[NEWLINE]')
            tmp['text'] = tmp['text'].replace('\n', '[NEWLINE]')
            r.append(tmp)
        return r

    async def ws_handler(self, ws, path):
        # 1. 클라이언트로부터 session_id 받기
        url = await ws.recv()
        print(url)
        if not url.startswith('https://www.youtube.com/watch?'):
            # 유튜브가 아니라면?
            return None

        video_id = url.split('watch?v=')[1].split('&')[0]
        print(video_id)
        subtitle = download_subtitle(video_id)
        print(len(subtitle))
        batch_size = 5
        for i in range(0, len(subtitle), batch_size):
            out = await self.predict(subtitle[i:i+batch_size])
            await ws.send('\n'.join(list(map(str, out))).replace("'", '"'))
            try:
                await ws.recv()
            except websockets.exceptions.ConnectionClosed:
                return None


if __name__ == "__main__":
    ws_server = wsServer('0.0.0.0', 2001, certfile="fullchain.pem", keyfile="privkey.pem")

