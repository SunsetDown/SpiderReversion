from math import floor
import execjs
import requests
import time


w = '+-a^+6'
url = 'https://fanyi.baidu.com/v2transapi'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Referer': 'https://fanyi.baidu.com/',
    'Cookie': 'BAIDUID=81B6588A59D26896775BF10BBEE1A491:FG=1; BAIDUID_BFESS=81B6588A59D26896775BF10BBEE1A491:FG=1; BDUSS=EYyRU9YaDdEa3RPRnF1dX5WVlJTZnI5ckRqZEJaaWN2bzJQbE9UVnFHbXNhVGxqSVFBQUFBJCQAAAAAAAAAAAEAAAALnsGAU0t5X01BRF9Kb2tlcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKzcEWOs3BFja; BDUSS_BFESS=EYyRU9YaDdEa3RPRnF1dX5WVlJTZnI5ckRqZEJaaWN2bzJQbE9UVnFHbXNhVGxqSVFBQUFBJCQAAAAAAAAAAAEAAAALnsGAU0t5X01BRF9Kb2tlcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKzcEWOs3BFja; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1662546698; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1662553373; ab_sr=1.0.1_YmEzYTQ0NTQxNzNlZTk4ZWY0NTVhNDk4MTllOTZhYzcxMGNiZjhmOWJlNWM1YzUwZGY1MDJhYTA4NjEzOGUyZTJmM2ZjZDBjNjc1MzE4M2FkMWU2YWNkY2QzYmE0YTIxNmI0ZWNlY2I2NDhiNTAzZTU5MjY0NGY4YjgxNmEwOGFlMDBmMmFmNGE0MDVlN2U5YTIwZDNmYjc5NDJlYzYzOGFlNzliYjBjOTNjYWJmY2I3NGI4NTBjMzExZjM2MDNj'
}

data = {
    'from': 'zh',
    'to': 'en',
    'transtype': 'realtime',
    'simple_means_flag': '3',
    'token': 'c39764708ae0ac5621ee1f0414e58a33',
    'domain': 'common'
}

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
        r = ctx.call('loca', t, r, 0)

        index = 0 if '+' == e[i] else 1
        t = ctx.call('cal', t, r, index)
    return t


def sign(b):
    k = "+-3^+b+-f"
    m = 131321201
    f = 320305
    print(b)
    b = encode(b, k)
    b ^= m
    if b < 0:
        b = 2147483648 + (2147483647 & b)
    b %= 1000000
    return f"{b % 1000000}.{b ^ f}"


def get_g(text):
    g = []
    for i in range(len(text)):
        _ = ord(text[i])
        if _ < 128:
            g.append(_)
        else:
            if _ < 2048:
                g.append(_ >> 6 | 192)
            else:
                if (55296 == (64512 & _) and i + 1 < len(text) and 56320 == (64512 & ord(text[i+1]))):
                    g.append(_ >> 12 | 224)
                    g.append(_ >> 6 & 63 | 128)
                    g.append(63 & _ | 128)
    return g


def get_sign(text):
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
    if kwargs:
        for key, value in kwargs.items():
            data[key.strip('_')] = value
    data['query'] = text
    data['sign'] = get_sign(text)
    for key, value in data.items():
        print(f'{key} : {value}')
    session = requests.session()
    json = session.post(url=url, data=data, headers=headers).json()
    try:
        return json['trans_result']['data'][0]['dst']
    except:
        # print(json)
        return '翻译失败'


if __name__ == '__main__':

    print(baidu_fanyi('power level', _from='en', to='zh'))
