import requests
import execjs
from time import time, sleep
import json
from pprint import pprint


def get_param(d,
              e="010001",
              f="00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7",
              g="0CoJUm6Qyw8W8jud"):
    with open('SpiderReversion/Music_163.js', 'r', encoding='utf-8')as file:
        ctx = execjs.compile(file.read())
    return ctx.call('copy', d, e, f, g)


def deal_resp(data: dict):
    def get_coment(data):
        return [{'评论': text['content'], '点赞数': text['likedCount'],
                '发布时间': text['timeStr'], '发布用户': text['user']['nickname']} for text in data]

    _data = data['data']['comments']
    coments = get_coment(_data)
    dealed = {
        '评论': coments,
    }
    try:
        _data = data['data']['hotComments']
        coments = get_coment(_data)
        dealed['热门评论'] = coments
    except:
        pass
    return dealed


def get_data(data):
    return get_param(json.dumps(data))


def get_comment(id, page=1, wait_time: float | None = 0):
    res = {
        '评论': [],
        '热门评论': []
    }
    session = requests.Session()
    session.get(f'https://music.163.com/#/playlist?id={id}')
    for i in range(1, page+1):
        url = 'https://music.163.com/weapi/comment/resource/comments/get'

        params = {
            "csrf_token": "df6d15163cd46c9216e6f374c98de9b3"
        }
        data = {
            "rid": f"A_PL_0_{id}",
            "threadId": f"A_PL_0_{id}",
            "pageNo": i,
            "pageSize": "20",
            "cursor": round(time()*1000),
            "offset": "0",
            "orderType": "1",
        }
        data["csrf_token"] = params["csrf_token"]
        data = get_data(data)
        data = {
            'params': data['encText'],
            'encSecKey': data['encSecKey']
        }

        resp = session.post(url, data, params=params)

        page_res = deal_resp(resp.json())
        if '热门评论' in page_res:
            res['热门评论'] += page_res['热门评论']
        res['评论'] += page_res['评论']
        sleep(wait_time)
    return res


if __name__ == "__main__":
    coment_163 = get_comment(777915656, 20)
    with open('SpiderData/Music163.json', 'w', encoding='utf-8')as f:
        f.write(json.dumps(coment_163, ensure_ascii=False))
