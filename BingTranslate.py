import requests
import re
from fake_useragent import UserAgent as ua


class Bing:
    session = requests.Session()
    times = 1
    headers = {
        'user-agent': ua().random
    }

    def __init__(self, text: str) -> None:
        self.text = text

    def deal_token(self, data: str):
        data = data.split(',')

        return [data[0].strip('"'), data[1].strip('"')]

    def get_token(self):
        url = 'https://cn.bing.com/translator?ref=TThis&from=en&to=zh-Hans&isTTRefreshQuery=1'

        pattren = re.compile(r'params_RichTranslateHelper = \[(.*?)\];')

        resp = self.session.get(url, headers=self.headers)
        res = pattren.findall(resp.text)[0]

        return self.deal_token(res)

    def bing_translate(self):
        url = f'https://cn.bing.com/ttranslatev3?isVertical=1&&IG=1B558B84854143D69302D7F8575CF95E&IID=translator.5022.{self.times}'


        data = {
            # '': '',
            'fromLang': 'en',
            'text': self.text,
            'to': 'zh-Hans',
        }

        data['key'], data['token'] = self.get_token()
        resp = self.session.post(url, data=data, headers=self.headers)
        self.times += 2
        if resp.status_code != 200:
            raise ValueError(data)
        return resp.json()[0]['translations'][0]['text']

    def __repr__(self) -> str:
        return self.bing_translate()

    __str__ = __repr__


print(Bing('a'))
