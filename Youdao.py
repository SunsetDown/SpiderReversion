import time
import random
import hashlib
import requests


def get_sign(e):
    t = str(round(time.time()*1000))
    i = t + str(round(random.random()*10))
    end = {
        'lts': t,
        'salt': i,
        'sign': hashlib.md5(f"fanyideskweb{e}{i}Ygy_4c=r#e#4EX^NUGUc5".encode()).hexdigest()
    }
    return end


def translate(text):
    args = get_sign(text)

    data = {
        'i': text,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': args['salt'],
        'sign': args['sign'],
        'lts': args['lts'],
        'bv': '01e27702dbb21a6d2b97645ec075ab88',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    headers = {
        'Host': 'fanyi.youdao.com',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-1255590839@10.112.57.87; OUTFOX_SEARCH_USER_ID_NCOO=61715945.7912438; ___rl__test__cookies=1662472705717',
        'Referer': 'https://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
    }

    url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    time.sleep(0.5)
    try:
        json = requests.post(url, data=data, headers=headers).json()
        try:
            return json["translateResult"][0][0]["tgt"]
        except:
            print(json)
            return '翻译失败'
    except:
        print('翻译失败')
        return '翻译失败'
