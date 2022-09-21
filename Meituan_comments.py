import requests
import json
from lxpy import copy_headers_dict


url = 'https://cd.meituan.com/meishi/api/poi/getMerchantComment'

session = requests.session()
headers = {
    'cookie': 'uuid=d83a781bd9654464b72d.1663577183.1.0.0; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _lxsdk_cuid=18354ed551dc8-0236116e70f4a6-613f5052-144000-18354ed551dc8; ci=59; __mta=212172331.1663577195005.1663577195005.1663577195005.1; client-id=69618dc9-1c9b-4652-b955-0c920c275e0a; mtcdn=K; userTicket=yeaiqzPVZeEjoUoPhOrbQNZTxTcxMtsHUQdyKpJP; _yoda_verify_resp=Y1kcwFMK9NG9qhG3FbFUeMXIn4ieYHLG2cIigWUdSFkucwRtjUl1rfwecorniFazU%2BcwTPlE3AJhXaT4QgZB490ENUFKxiOIt2OivYCaY6qDYgYCOnBeOtwAqEJqmj0rExWIGcDUUNOkEMKwoMw5kGLrX4AmrY4oEUX4%2FJOld06F%2BhYa%2F1qKP%2BNzVsPxA%2FxeiNtaEvIgINmzoTvQNx2iZx2555vI%2BNz5xFQ5Ot88qBmRrj8e5fu6gnCCXaZUZJWMJ8%2FvZ1uHRLMnIkTm%2FmSCgEBHa3%2Fc4cYZuC8O%2BHeATqws2ZVC8AdOIa7jJmJArt3DVu9bPR0y5%2BbO%2FI3Sfcei3KKUdsFZzN8rtFjFJGMoVJ5U9P%2F%2F1OlNTP1YyokKsB%2FT; _yoda_verify_rid=15d0184944c2605d; u=997805152; n=%E5%A4%95%E9%98%B3%E8%A5%BF%E4%B8%8B%E6%AC%A7%E5%B0%BC%E9%85%B1; lt=30SR7DnbLXMd90VVaioBosNwprgAAAAACRQAABqLX_XicRdEJh-Z7uuDxr8_Cs82MQBpH_W8no9c5rJhDlb0olJLM43kA2zyhgRjaA; mt_c_token=30SR7DnbLXMd90VVaioBosNwprgAAAAACRQAABqLX_XicRdEJh-Z7uuDxr8_Cs82MQBpH_W8no9c5rJhDlb0olJLM43kA2zyhgRjaA; token=30SR7DnbLXMd90VVaioBosNwprgAAAAACRQAABqLX_XicRdEJh-Z7uuDxr8_Cs82MQBpH_W8no9c5rJhDlb0olJLM43kA2zyhgRjaA; token2=30SR7DnbLXMd90VVaioBosNwprgAAAAACRQAABqLX_XicRdEJh-Z7uuDxr8_Cs82MQBpH_W8no9c5rJhDlb0olJLM43kA2zyhgRjaA; unc=%E5%A4%95%E9%98%B3%E8%A5%BF%E4%B8%8B%E6%AC%A7%E5%B0%BC%E9%85%B1; _lxsdk=18354ed551dc8-0236116e70f4a6-613f5052-144000-18354ed551dc8; WEBDFPID=uy5656uy656z5zyz0w8uy954v1v5111481645vv2vw5979584vy1zz62-1978937259299-1663577258862IQQQWASfd79fef3d01d5e9aadc18ccd4d0c95073707; _hc.v=034ac5ff-5ca9-4ed3-4e27-91e57e73d7df.1663577259; lat=30.663331; lng=104.084123; _lxsdk_s=18354ed551e-8aa-287-173%7C%7C26; firstTime=1663577275598',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
    'mtgsig': '{"a1":"1.0","a2":1663577365811,"a3":"uy5656uy656z5zyz0w8uy954v1v5111481645vv2vw5979584vy1zz62","a4":"7fb8e7484b8cf44b48e7b87f4bf48c4b7bfa482b300ec460","a5":"1ZR3cm4lCo2IKgdmf0P7GmeCBQHaZPSTUJnqRQK2le2yQOJZ/XRT+P5S/4JtNxK5MCTqMOPPSjkXv21q3sRuHRtt+23Kl/qtmrIw6UPcW+acPzVDsh3e2VJ7nIxb1mLrZ2V=","a6":"h1.2yM2vpoQOQClU2zLi/d0UHA9IKDNqRazec4rjjPqtYs6WXJC0K6jpWJ4o7IswH94LWUUYNl9tP9jMtCtWe0h3WH1oH74rSXOQloRtn5i9td/EUVyogLzA1JFkfwRDOXnXKuOcj5LRAaIe8ozO4ttrpM83lw2nBWw419fpJS7Pf5p/ZUjVCn8oKEBpQ+MirvoVHPQPUJ7rdPhzbKR7ORV9YoGb0AJBlUxsaDNpvIO94bfp7TUDUUhXQSZaV9hvJqMCaqIQkZI5RTCzLoJBJ1GUHne2IcwNuiN5YSF2hoDeXh0xyBQgA+JJd3czmtcX3OS2r9abXW8OCqw3tIMA3SRLZd2tJ+XswnvVXJp1Py6i2a5bWgXYeWCvQkwofV/l0Vq/onlQneDDYD+pHm/ShbUq+se0sPehl/QToM6KpRqIwidNZMgdNw5tNAW/MnXLuIWcDBB7k/w7oCywjkvNlH6TsjXjunBUtfW5fYOZutCX2VRFuoDt3sLlnp2Tjyu+PDkCptxcfEB02YJNE8edZSroFCmhGf0kejXuwaZcEPGpOcyceVdpJigyfoA+7DRIGrBjWaq9/EulfiCDDvup+Uevctoaz7MDweJMM5wLMiqXDTrt4H+cODG+m1a+OuY5dGsNMMTT2bAeoUfPodaMR5D+Cl3D+Lo+jkvZzzuzPMxKwgdbrvEcku3oyp07hcPAHOdEA5nub9RhsOMo+eK/ZScZ0ho8xOyZSr9x7hIrgIMs+TY=","a7":"com.sankuai.web.meishife.pcweb","x0":4,"d1":"84a107fbbf761b1a51c5abcbdb3dd196"}'
}

params = '''
uuid: d83a781bd9654464b72d.1663577183.1.0.0
platform: 1
partner: 126
originUrl: https://cd.meituan.com/meishi/97195179/
riskLevel: 1
optimusCode: 10
id: 97195179
userId: 997805152
offset: 10
pageSize: 10
sortType: 1
tag: 
'''

params = copy_headers_dict(params)

resp = session.get(url, params=params, headers=headers)

print(resp.json())
