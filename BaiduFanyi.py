from math import floor
import execjs
import requests
from fake_useragent import UserAgent as ua
import re


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
    data['sign'] = jscode_sign(text)

    url = 'https://fanyi.baidu.com/v2transapi'
    resp = session.post(url=url, data=data, headers=headers)

    try:
        return resp.json()['trans_result']['data'][0]['dst']
    except:
        print(resp.text)
        return '翻译失败'


def jscode_sign(text):
    _jscode = r'''
    function n(t, e) {
    for (var n = 0; n < e.length - 2; n += 3) {
        var r = e.charAt(n + 2);
        r = "a" <= r ? r.charCodeAt(0) - 87 : Number(r),
            r = "+" === e.charAt(n + 1) ? t >>> r : t << r,
            t = "+" === e.charAt(n) ? t + r & 4294967295 : t ^ r
    }
    return t
    }
    function sign(t) {
    var o, i = t.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g), r = '320305.131321201';
    if (null === i) {
        var a = t.length;
        a > 30 && (t = "".concat(t.substr(0, 10)).concat(t.substr(Math.floor(a / 2) - 5, 10)).concat(t.substr(-10, 10)))
    } else {
        for (var s = t.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), c = 0, u = s.length, l = []; c < u; c++)
            "" !== s[c] && l.push.apply(l, function (t) {
                if (Array.isArray(t))
                    return e(t)
            }(o = s[c].split("")) || function (t) {
                if ("undefined" != typeof Symbol && null != t[Symbol.iterator] || null != t["@@iterator"])
                    return Array.from(t)
            }(o) || function (t, n) {
                if (t) {
                    if ("string" == typeof t)
                        return e(t, n);
                    var r = Object.prototype.toString.call(t).slice(8, -1);
                    return "Object" === r && t.constructor && (r = t.constructor.name),
                        "Map" === r || "Set" === r ? Array.from(t) : "Arguments" === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? e(t, n) : void 0
                }
            }(o) || function () {
                throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
            }()),
                c !== u - 1 && l.push(i[c]);
        var p = l.length;
        p > 30 && (t = l.slice(0, 10).join("") + l.slice(Math.floor(p / 2) - 5, Math.floor(p / 2) + 5).join("") + l.slice(-10).join(""))
    }
    for (var d = "".concat(String.fromCharCode(103)).concat(String.fromCharCode(116)).concat(String.fromCharCode(107)), h = (null !== r ? r : (r = undefined || "") || "").split("."), f = Number(h[0]) || 0, m = Number(h[1]) || 0, g = [], y = 0, v = 0; v < t.length; v++) {
        var _ = t.charCodeAt(v);
        _ < 128 ? g[y++] = _ : (_ < 2048 ? g[y++] = _ >> 6 | 192 : (55296 == (64512 & _) && v + 1 < t.length && 56320 == (64512 & t.charCodeAt(v + 1)) ? (_ = 65536 + ((1023 & _) << 10) + (1023 & t.charCodeAt(++v)),
            g[y++] = _ >> 18 | 240,
            g[y++] = _ >> 12 & 63 | 128) : g[y++] = _ >> 12 | 224,
            g[y++] = _ >> 6 & 63 | 128),
            g[y++] = 63 & _ | 128)
    }
    for (var b = f, w = "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(97)) + "".concat(String.fromCharCode(94)).concat(String.fromCharCode(43)).concat(String.fromCharCode(54)), k = "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(51)) + "".concat(String.fromCharCode(94)).concat(String.fromCharCode(43)).concat(String.fromCharCode(98)) + "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(102)), x = 0; x < g.length; x++)
        b = n(b += g[x], w);
    return b = n(b, k),
        (b ^= m) < 0 && (b = 2147483648 + (2147483647 & b)),
        "".concat((b %= 1e6).toString(), ".").concat(b ^ f)
    }
    '''
    ctx = execjs.compile(_jscode)
    return ctx.call('sign', text)


def pycode_sign(text):
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

    return get_sign(text)
