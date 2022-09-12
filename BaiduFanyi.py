from math import floor
import execjs
import requests
from fake_useragent import UserAgent as ua
import re


jscode = '''
function un(a, b) {
    return a ^ b
}


function loca(a, b, index) {
    return index == 0 ? a >>> b : a << b
}

function cal(a, b, index) {
    return index == 0 ? a + b & 4294967295 : a ^ b
}
'''


ctx = execjs.compile(jscode)


def encode(t, e):
    for i in range(0, len(e)-2, 3):
        r = e[i+2]
        r = ord(r) - 87 if ord('a') <= ord(r) else int(r)

        index = 0 if '+' == e[i+1] else 1
        r = ctx.call('loca', t, r, index)

        index = 0 if '+' == e[i] else 1
        t = ctx.call('cal', t, r, index)
    return t


def sign(b):
    k = "+-3^+b+-f"
    m = 131321201
    f = 320305
    b = encode(b, k)
    b ^= m
    if b < 0:
        b = 2147483648 + (2147483647 & b)
    b %= 1000000
    return f"{b % 1000000}.{b ^ f}"


def get_g(text):
    g = []
    i = 0
    while i < len(text):
        _ = ord(text[i])
        if _ < 128:
            g.append(_)
        else:
            if _ < 2048:
                g.append(_ >> 6 | 192)
            else:
                if (55296 == (64512 & _) and i + 1 < len(text) and 56320 == (64512 & ord(text[i+1]))):
                    i += 1
                    _ = 65536 + (((1023 & _) << 10) & 0XFFFFFFFF) + \
                        (1023 & ord(text[i]))
                    g.append(_ >> 18 | 240)
                    g.append(_ >> 12 & 63 | 128)
                else:
                    g.append(_ >> 12 | 224)
                    g.append(_ >> 6 & 63 | 128)
                    g.append(63 & _ | 128)
        i += 1

    return g


def get_sign(text):
    w = '+-a^+6'
    a = len(text)
    if a > 30:
        half = floor(a / 2) - 5
        text = text[0:10]+text[half:half+10]+text[-10:]
    b = 320305
    g = get_g(text)

    for i in g:
        b += i
        b = encode(b, w)

    return sign(b)


def baidu_fanyi(text, **kwargs):
    session = requests.session()

    url = 'https://fanyi.baidu.com/'

    headers = {
        'User-Agent': ua().random,

    }

    resp = session.get(url, headers=headers).text
    resp = session.get(url, headers=headers).text
    token = re.findall(r"token: '(.*?)',", resp)[0]
    print(token)

    data = {
        'from': 'zh',
        'to': 'en',
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'token': token,
        'domain': 'common'
    }

    if kwargs:
        for key, value in kwargs.items():
            data[key.strip('_')] = value

    data['query'] = text
    data['sign'] = get_sign(text)


    url = 'https://fanyi.baidu.com/v2transapi'
    resp = session.post(url=url, data=data, headers=headers)

    try:
        return resp.json()['trans_result']['data'][0]['dst']
    except:
        print(resp.text)
        return '翻译失败'


if __name__ == '__main__':
    res = baidu_fanyi('零基础入门')
    print(res)
    # a = encode(-1339786482, w)
    # print(a)
