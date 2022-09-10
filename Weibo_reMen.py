from random import randint
from time import strftime
import requests
from fake_useragent import UserAgent as ua
import re




def getVfromD(data: dict) -> str:
    dealed = ''
    stripHref = re.compile(r'<.*?>', flags=re.S)
    for text in data['data']['cards']:
        create_time = text['mblog']['created_at']
        writer = text['mblog']['user']['screen_name']
        title = text['mblog']['text']
        title = stripHref.sub('', title)
        dealed += f'作者: {writer}, 标题: {title}, 发布时间: {create_time},\n'
    return dealed.strip(',\n')


def get_weibo_json(page=1) -> requests.Response:
    url = 'https://m.weibo.cn/api/container/getIndex'

    headers = {
        'user-agent': ua().random
    }

    param = {
        'containerid': 102803,
        'openApp': 0,
        'since_id': page
    }

    resp = requests.get(url, param, headers=headers)
    return resp



resp = get_weibo_json(randint(1, 20))

if resp.status_code == 200:
    t = strftime("%y年%m月%d日%H时%M分%S秒")
    data = getVfromD(resp.json())
    with open(f'Weibo_reMen_{t}.text', 'a', encoding='utf-8') as f:
        f.write(f'\n{data}\n')
else:
    print(resp.text[:200])
    print('访问出错')
