import sys
sys.path.append('E:\PyProjects\SpiderReversion')
if True:
    from BingTranslate import Bing
    from Youdao import translate
    from BaiduFanyi import baidu_fanyi


baidu_trans = baidu_fanyi
youdao_trans = translate
bing_trans = Bing

