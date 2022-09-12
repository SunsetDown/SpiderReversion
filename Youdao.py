import time
import random
import hashlib
import requests
from fake_useragent import UserAgent as ua


def get_sign(e):
    t = str(round(time.time()*1000))
    i = t + str(round(random.random()*10))
    end = {
        'lts': t,
        'salt': i,
        'sign': hashlib.md5(f"fanyideskweb{e}{i}Ygy_4c=r#e#4EX^NUGUc5".encode()).hexdigest()
    }
    return end


def translate(text: str):
    args = get_sign(text)

    UA = ua().random

    data = {
        'i': text,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': args['salt'],
        'sign': args['sign'],
        'lts': args['lts'],
        'bv': hashlib.md5(UA.encode()).hexdigest(),
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    headers = {
        'Host': 'fanyi.youdao.com',
        'Cookie': f'OUTFOX_SEARCH_USER_ID=-1255590839@10.112.57.87; OUTFOX_SEARCH_USER_ID_NCOO=61715945.7912438; ___rl__test__cookies={args["lts"]}',
        'Referer': 'https://fanyi.youdao.com/',
        'User-Agent': UA
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
