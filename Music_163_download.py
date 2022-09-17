import requests
import json
from Music_163_params import get_param
import os


def download_song(id, name='music', path='SpiderData/163Music/'):
    url = 'https://music.163.com/weapi/song/enhance/player/url/v1'

    data = {
        "ids": f"[{id}]",
        "level": "standard",
        "encodeType": "aac",
        "csrf_token": "df6d15163cd46c9216e6f374c98de9b3"
    }
    data = json.dumps(data)

    data = get_param(data)

    data = {
        'params': data['encText'],
        'encSecKey': data['encSecKey']
    }
    params = {
        "csrf_token": "df6d15163cd46c9216e6f374c98de9b3"
    }

    resp = requests.post(url, data=data, params=params).json()

    url = resp['data'][0]['url']
    if url == None:
        raise ValueError(f'{name}目前不支持下载')

    resp = requests.get(url)
    with open(f'{path}/{name}.mp3', 'wb')as f:
        f.write(resp.content)


def from_list_download(id):
    url = 'https://music.163.com/weapi/v6/playlist/detail'

    params = {
        "csrf_token": "df6d15163cd46c9216e6f374c98de9b3"
    }

    data = {
        "id": f"{id}",
        "offset": "0",
        "total": "true",
        "limit": "1000",
        "n": "1000",
        "csrf_token": "df6d15163cd46c9216e6f374c98de9b3"
    }

    data = get_param(json.dumps(data))

    data = {
        'params': data['encText'],
        'encSecKey': data['encSecKey']
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
        'referer': 'https://music.163.com/my/',
        'cookie': '_ntes_nuid=28f75071417ae50afc9ab7ecc50753a0; NMTID=00Ojozfshmsj2PhzEI8v09go9wbtK0AAAF6tvSXAA; WEVNSM=1.0.0; WNMCID=bjaklk.1626567121425.01.0; WM_TID=Sl%2F7C%2Fegv%2B5ARABRRBd7jZ84v2HWyZxr; ntes_kaola_ad=1; _ntes_nnid=28f75071417ae50afc9ab7ecc50753a0,1656118144749; __snaker__id=Mh3I8sdzcQLczmt8; _9755xjdesxxd_=32; YD00000558929251%3AWM_TID=3y77SbASnPFFFFQAVQPUWPeq6WtzFVLu; YD00000558929251%3AWM_NI=sDpr4euxyBt5T3eo7JFEMxqHO%2BAKu03AEcztRDZ%2BJZQEP7t6kZFimizKCUG1HlRDaD1L7yB%2BS5BQBRG5Fn6QjVDIdeZLJ4a35JkOUgQPA8Wxk5kONqmhyMPnenxq%2Fz1reWw%3D; YD00000558929251%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee8fe4809a8bfd89db79bc968fb2d54b839f9a82c844f3ac88d7cd3eb4bb9ab6f92af0fea7c3b92ab19cc093b76fb7a8b7a3f73f98edab90b642869b8399f4448df58facf83cf19f8b84f980929c96ccc952939ba0d8f73ea9868a8af063ba958db6c63b8cb49ea5e450f394f99ac12191eb8eb2c15a85eb8a8fb55baa8a8caae76f9a9486d5e439f796a5b0d86d93908fd9d674a9eba5b0cd7bafb8b7aed366a7b2b892ae72f3aeabb8f637e2a3; MUSIC_U=330457a2b0a0024fe66838f9c57d17463851927dfcefa2ee0a3819db6cf2cbd3993166e004087dd3e198320860bf8ac418abdc0dc16f7966129b661b1377decdbb1fa89b8b957f2dd4dbf082a8813684; __csrf=df6d15163cd46c9216e6f374c98de9b3; gdxidpyhxdE=W3a1QapD0Vh1ZteV69%2Bq2QYBinXbPkpKQIX8JB5lC9Xo5yDtNyR9jriEYlI7kVGhykn7I1cTxUUUkcGYSHBG7C8l2HkE54A%2FPJiEnyCMMCQjY%5CMbEn2uq%5C%5CdmCMQSlPVeCaiYbROzyT%2FtxqX8fN3fjqVreNbMoTIBQGErRdiDZ3uLC5g%3A1663049341802; _iuqxldmzr_=32; WM_NI=26s6%2Bys%2B2eNlKLRP%2Bg%2FgogL%2Fdb2hFKBGJSZTOhpHLxpbYv78iK7r7%2BxkVRaDwhzIsFrdeMIgDAKTcQvUFBLvkqHQTlgOl6JoQ9xhbKp%2F2kzAJkEKImu6rXKMG3YAFZLFbEU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee98b44baeb2ac91d03e93868aa3d15e869b9e87d550bb9c84a4f26e839b84b0f32af0fea7c3b92af2eabdd7aa73b1f5fe86cd6889949eb1aa6dedb9a188cf25a8befe89c541829986b4d9608db8c0a9cf74b4be9797b634ab95f993b621bcb59ab3e450b5b8b6aaf24eb2bcabaecc6d889f85b5e25bb68b8aa3cf7ea9af88b2d768a591a4d7c96593e7b889e141b4f1fe8cf94b8ab58baccc67b7eabeb9ca4785ed97a2c552909aaea6d837e2a3; playerid=88792982; JSESSIONID-WYYY=V%5CaBFoo8C67ngzagGj2Sf6MKMvAmkQmM%2B0Uwrz%2FS305fs%5CmbPStcM4fBlMmXMIipkMZ%5Cr%2F3%2BONNCMBO%5CsX60rIQ19og%2FM5xyc7eI%2F%5C%5CeadVa3mnPraEGZHiWNahgt0b8hpIoIEBbWC1dpKp018thC6JRt%5CKh49%2FO0HvepeTGitqBDQ5D%3A1663423621916'
    }

    resp = requests.post(url, data=data, params=params,
                         headers=headers).json()

    path = f"SpiderData/163Music/{resp['playlist']['name']}"

    if not os.path.exists(path):
        os.mkdir(path)

    for i, content in enumerate(resp['playlist']['tracks']):
        title = str(i+1) + '.' + content['name'] + '_'
        ars = []
        for ar in content['ar']:
            ars.append(ar['name'] if ar['name'] else '未知')
        title += '-'.join(ars)
        id = content['id']

        try:
            download_song(id, title, path)
            print(f'{title}下载成功!!!')
        except Exception as er:
            print(f'{title}下载失败!!!')
            print(er)


if __name__ == '__main__':
    from_list_download(2571564867)
