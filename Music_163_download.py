import requests
import json
from Music_163_params import get_param
import os
import re


syspath = os.getcwd()
path = os.path.join(syspath, 'SpiderData/163Music/')

if not os.path.isdir(path):
    if not os.path.isdir(os.path.join(syspath, 'SpiderData/')):
        os.mkdir(os.path.join(syspath, 'SpiderData/'))
    os.mkdir(path)


def download_song(id, name='music', path=path):
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
        "csrf_token": "dbe62e7bf8d62354fd7b051f4524ad72"
    }

    data = {
        "id": f"{id}",
        "offset": "0",
        "total": "true",
        "limit": "1000",
        "n": "1000",
        "csrf_token": "dbe62e7bf8d62354fd7b051f4524ad72"
    }

    data = get_param(json.dumps(data))

    data = {
        'params': data['encText'],
        'encSecKey': data['encSecKey']
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
        'referer': 'https://music.163.com/my/',
        'cookie': '_ntes_nnid=477845777e0e0b6afc736a03887c485a,1656037203206; _ntes_nuid=477845777e0e0b6afc736a03887c485a; NMTID=00O0D_p_yGEfmLZ1EQWoBiw6Z_ebZIAAAGBk4Jd2w; WNMCID=seqhxe.1656037203894.01.0; WEVNSM=1.0.0; WM_TID=mdb/7Yp5zbZAUREVFBLEV5ZPwBhoJWvL; ntes_kaola_ad=1; WM_NI=l+KWFvE8kIIQnHkoxr7ssLzM5E9KaL+lQzqXOqaKb4zEWWqJNYZmN10FTzAQzWg+cLtTDffy/jGVMwD2fNwQdr8m1kmX1PWm0mVaPXlqs8Omp5v4ygqjDbDGYFr0Wuz1QUQ=; WM_NIKE=9ca17ae2e6ffcda170e2e6eeadf14af28f8797c54eadbc8ea7d84e838f9b87c859b8afba8db25cf193aeb6e42af0fea7c3b92ab0f585b8c57e87e8a5aacc5bae98a590fb7af5adbdadf947f79bf7ace448e9b49f9bf4548dafaface140ba9b99b8f4428e87968ecd3bf49a9c9bc45bba89a9cce248b88c8c87e573edb689b7d07d88eeaaaff65ba8aef88eb461af88ffb1d667f4b39a82d354b0afbdd9ce67b4ebbad5fc6db3b68c83c74d9b9abed1d67fbaef9fb6d437e2a3; __snaker__id=yiLtuFmNgL0DMuHa; _9755xjdesxxd_=32; YD00000558929251:WM_NI=Csa+9RgwSMc7QpYxVL6GmyABHMWJmk1JXUu+6/hO7a/7MLAUoy4KnHlMEh61fcLMwkQxKrMY4na0DpWJWhqLMw8mbWQz5vreQpqHvcBAttKXATRlgdhCz5QyufH3vYpidFc=; YD00000558929251:WM_NIKE=9ca17ae2e6ffcda170e2e6eed1ea25aaabba86f95df89e8ea3d44e929b8bb1c860f8f1ba89b26faeef96d9e22af0fea7c3b92a81adafccbc5aa5a99daee23d93b09799d548f699a39ac44a8c9399abf061f39698b6f821f6f1a8b0b66bede983adc45fada7fcaced44b0938b89b53ba6bd84aef66193a88593d053f8b2afd1c77c95969989f4488fa9f88ee15d93a6fb97f16f93b0bfa9f569829fbc95ca54838c9e8de670ac9db6d6d473b7ba88d4f553b4b7aca7e237e2a3; YD00000558929251:WM_TID=uUHu24qWm+dEAEAEREKEX5q60jajgd5M; JSESSIONID-WYYY=rUUBcFFZC5\7hcaxbAiS3FVdMq8clDUy3onTsBFSDKhkyoXqyOgWQjaDpfhRuN5pezk4T4dZhMsXWGmMGO30n6jvmVFiuMCuWG3wlipUtV9x6wn6gjCbOgmmjC4nca0l6Bb4FVYWcQ0JbEq/hJSbM3ngtkj1Zhtg5qav7mCPiP6ztQs4:1665370150981; _iuqxldmzr_=33; gdxidpyhxdE=9J0V5CrcnvO0mzEypdVhtUEnMGeBKQ8h8raaYexsO4\LbEIm/MyGRD7pHvN35RCVuSSN3nWqH0I+KK3TpaR0sJZ9yhShcoiqzSxAu7kVIHYPU/PtcrRRukf8RYvWDIJfKP6eK9Lz0ZmREsgNgTIy5C2vi/dO9RgyvABkOE8ueQlwndgc:1665370033914; MUSIC_U=330457a2b0a0024fe66838f9c57d1746c5c054eb9bb86fbf3336d3770f295f58993166e004087dd3f7e30da268260ff44184356db009c68c129b661b1377decdbb1fa89b8b957f2dd4dbf082a8813684; __csrf=dbe62e7bf8d62354fd7b051f4524ad72'
    }

    resp = requests.post(url, data=data, params=params,
                         headers=headers).json()

    _path = os.path.join(path, resp['playlist']['name'])

    if not os.path.exists(_path):
        os.mkdir(_path)

    for i, content in enumerate(resp['playlist']['tracks']):
        title = str(i+1) + '.' + content['name'] + '_'
        ars = []
        for ar in content['ar']:
            ars.append(ar['name'] if ar['name'] else '未知')
        title += '-'.join(ars)
        id = content['id']

        try:
            download_song(id, title, _path)
            print(f'{title}下载成功!!!')
        except Exception as er:
            print(f'{title}下载失败!!!')
            print(er)


def from_album_download(id):
    url = f'https://music.163.com/album?id={id}'

    resp = requests.get(url)

    data = re.findall(
        r'<textarea id="song-list-pre-data" style="display:none;">(.*?)</textarea>', resp.text)[0]
    data = json.loads(data)

    ablum_name = re.findall(r'"title": "(.*?)",', resp.text)[0]

    _path = os.path.join(path, ablum_name)
    if not os.path.exists(_path):
        os.mkdir(_path)

    for i, content in enumerate(data):
        title = str(i+1) + '.' + content['name'] + '_'
        ars = []
        for ar in content['artists']:
            ars.append(ar['name'] if ar['name'] else '未知')
        title += '-'.join(ars)
        id = content['id']

        try:
            download_song(id, title, _path)
            print(f'{title}下载成功!!!')
        except Exception as er:
            print(f'{title}下载失败!!!')
            print(er)


def download(url: str):
    if 'album' in url:
        from_album_download(url.split('=')[-1])
    elif 'playlist' in url:
        from_list_download(url.split('=')[-1])
    elif 'song' in url:
        download_song(url.split('=')[-1])
