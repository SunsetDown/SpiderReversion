import requests
import json
from time import time, strftime
import zlib
import base64


class PageError(Exception):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'页数不能小于1, 没有 {self.value} 页， 请输入其他起始页数'

    __str__ = __repr__


class MeiTuan:
    url = 'https://cd.meituan.com/meishi/api/poi/getPoiList'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Referer': 'https://cd.meituan.com/meishi/',
        'Cookie': 'uuid=6b176f55b6484909984a.1662703270.1.0.0; _lxsdk_cuid=18320d6795ac8-0a1f8b6b234e96-26021c51-232800-18320d6795a2b; ci=59; client-id=7dc47f23-b482-4988-8b07-a3b589b43004; mtcdn=K; IJSESSIONID=node0yf5wisiqh314ndzdt918pvc5179657658; iuuid=CC996C0FD08231585D6B152C971CDB0CD2712002B0CBD7CEF212DF6932DB81C5; cityname=%E6%88%90%E9%83%BD; _lxsdk=CC996C0FD08231585D6B152C971CDB0CD2712002B0CBD7CEF212DF6932DB81C5; _lx_utm=utm_source%3DMTPCmain-4; __mta=222187815.1662703275703.1662727475310.1662727554758.9; lt=xllyiBlp9LdtR_747JmE6ZfLnzgAAAAAxhMAAOaGcQEI5rigQ-TCCNA388IZHzyuYzuSwaAEwLi8NEeF7oJju60XH0t7NJDNrMf_qw; u=997805152; n=%E5%A4%95%E9%98%B3%E8%A5%BF%E4%B8%8B%E6%AC%A7%E5%B0%BC%E9%85%B1; token2=xllyiBlp9LdtR_747JmE6ZfLnzgAAAAAxhMAAOaGcQEI5rigQ-TCCNA388IZHzyuYzuSwaAEwLi8NEeF7oJju60XH0t7NJDNrMf_qw; firstTime=1662727602804; unc=%E5%A4%95%E9%98%B3%E8%A5%BF%E4%B8%8B%E6%AC%A7%E5%B0%BC%E9%85%B1; _lxsdk_s=1832245f7e4-fdf-829-48c%7C%7C36'
    }

    param = {
        'cateId': 0,
        'areaId': 0,
        'sort': '',
        'dinnerCountAttrId': '',
        'page': 1,
        'userId': 997805152,
        'uuid': '6b176f55b6484909984a.1662703270.1.0.0',
        'platform': 1,
        'partner': 126,
        'originUrl': 'https://cd.meituan.com/meishi/',
        'riskLevel': 1,
        'optimusCode': 10
    }

    session = requests.session()

    def __init__(self, cityname='成都'):
        self.param['cityName'] = cityname

    def encode(self, data):
        data = zlib.compress(data)
        data = base64.b64encode(data)
        return str(data, encoding='utf-8')

    @property
    def deal_param(self):
        obj = dict(sorted(self.param.items(), key=lambda a: a[0]))
        end = ''
        for key, value in obj.items():
            end += f'{key}={value}&'
        return end.strip('&').encode()

    def __token(self):

        iP = {
            "rId": 100900,
            "ver": "1.0.6",
            "ts": time(),
            "cts": time()+2300,
            "brVD": [1872, 401],
            "brR": [[1920, 1200], [1920, 1152], 24, 24],
            "bI": ["https://cd.meituan.com/meishi/", "https://cd.meituan.com/"],
            "mT": [],
            "kT": [],
            "aT": [],
            "tT": [],
            "aM": "",
            "sign": self.encode(self.deal_param)
        }
        return self.encode(json.dumps(iP).encode())

    def token(self):
        self.param['_token'] = self.__token()

    def save2file(self, data):
        try:
            data = dict(data)
        except:
            pass

        data = json.dumps(data, ensure_ascii=False)
        t = strftime("%y年%m月%d日%H时%M分%S秒")

        with open(f'meituan_{t}.json', 'w', encoding='utf-8') as f:
            f.write(f'\n{data}\n')
        print("Done!!!!")

    def __page(self, page):
        data = []
        self.token()

        for _ in range(page):
            resp = self.session.get(
                self.url, params=self.param, headers=self.headers)
            data.append((f'page_{self.param["page"]}', resp.json()))
            self.param['page'] += 1

        self.save2file(data)

    def __index(self):
        self.token()
        resp = self.session.get(
            self.url, params=self.param, headers=self.headers)

        self.save2file(resp.json())

    def run(self, page=0, startpage=1):
        if startpage > 1:
            self.param['page'] = startpage
        elif startpage < 1:
            raise PageError(startpage)
        if page:
            self.__page(page)
        else:
            self.__index()


def decode_token(data):
    data = base64.b64decode(data.encode())
    data = zlib.decompress(data).decode('utf-8')
    print(data)

    sign = json.loads(data)['sign']
    decode_token(sign)


MeiTuan().run(10, 5)
