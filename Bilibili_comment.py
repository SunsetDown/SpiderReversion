import requests
import re
import json
from fake_useragent import UserAgent as ua


class BilibiliComment:
    session = requests.Session()
    headers = {
        'user-agent': ua().random
    }
    next = 0
    data = []

    def __init__(self, url: str) -> None:
        self.url = url

    def get_oid(self):
        pattren = re.compile(r'window.__INITIAL_STATE__={"aid":(.*?),"bvid"')

        resp = self.session.get(self.url, headers=self.headers)

        self.oid = pattren.findall(resp.text)[0]

    def get_comments(self):
        url = 'https://api.bilibili.com/x/v2/reply/main'

        params = {
            'mode': 3,
            'next': self.next,
            'oid': self.oid,
            'plat': 1,
            'type': 1,
        }
        resp = self.session.get(
            url, params=params, headers=self.headers).json()

        for comment in resp['data']['replies']:
            data = {'message': comment['content']['message'],
                    'like': comment['like'],
                    'user': {
                        'name': comment['member']['uname'],
                        'mid': comment['member']['mid'],
                        'sign': comment['member']['sign'],
                        'sex': comment['member']['sex']
            }
            }
            if comment['replies']:
                data['reply_to_the_comment'] = [{
                    'message': content['content']['message'],
                    'like': content['like'],
                    'user': {
                        'name': content['member']['uname'],
                        'mid': content['member']['mid'],
                        'sign': content['member']['sign'],
                        'sex': content['member']['sex']
                    }
                } for content in comment['replies']]
            self.data.append(data)

    def save2local(self):
        data = json.dumps(self.data, ensure_ascii=False)
        with open('SpiderData/bilibili_comment.json', 'w', encoding='utf-8')as f:
            f.write(data)

    def run(self, page=1):
        self.get_oid()
        for i in range(page):
            self.get_comments()
            self.next += 1
            if self.next == 1:
                self.next += 1
        self.save2local()
        print('Done!!!')
        print(self.next)
