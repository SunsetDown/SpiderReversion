import requests
import re


class Bing:
    session = requests.Session()
    times = 1

    def __init__(self, text: str) -> None:
        self.text = text

    def deal_token(self, data: str):
        data = data.split(',')

        return [data[0].strip('"'), data[1].strip('"')]

    def get_token(self):
        url = 'https://cn.bing.com/translator?ref=TThis&from=en&to=zh-Hans&isTTRefreshQuery=1'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33'
        }

        pattren = re.compile(r'params_RichTranslateHelper = \[(.*?)\];')

        resp = self.session.get(url, headers=headers)
        res = pattren.findall(resp.text)[0]

        return self.deal_token(res)

    def bing_translate(self):
        url = f'https://cn.bing.com/ttranslatev3?isVertical=1&&IG=1B558B84854143D69302D7F8575CF95E&IID=translator.5022.{self.times}'

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33'
        }

        data = {
            # '': '',
            'fromLang': 'en',
            'text': self.text,
            'to': 'zh-Hans',
        }

        data['key'], data['token'] = self.get_token()
        resp = self.session.post(url, data=data, headers=headers)
        self.times += 2
        if resp.status_code != 200:
            raise ValueError(data)
        return resp.json()[0]['translations'][0]['text']

    def __repr__(self) -> str:
        return self.bing_translate()

    __str__ = __repr__


print(Bing('a'))
