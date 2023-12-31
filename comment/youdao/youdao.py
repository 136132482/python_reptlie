import hashlib
import random
import time
import requests


datas={
'中文':'zh',
'英语':'en',
'日语':'ja',
'韩语':'ko',
'法语':'fr',
'德语':'de',
'俄语' :'ru',
'西班牙语':'se',
'葡萄牙语':'pt',
'意大利语':'it',
'越南语':'vi',
'印尼语':'id',
'阿拉伯语':'ar',
'荷兰语':'nl',
'泰语':'th'
}

def send_request(content,to_lang):
    salt = str(round(time.time() * 1000)) + str(random.randint(0, 9))
    data = "fanyideskweb" + content + salt + "Tbh5E8=q6U3EXe+&L[4c@"
    sign = hashlib.md5()
    sign.update(data.encode("utf-8"))
    sign = sign.hexdigest()

    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        'Cookie': 'OUTFOX_SEARCH_USER_ID=-1927650476@223.97.13.65;',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    }
    data = {
        'i': str(content),
        'from': 'AUTO',
        'to': to_lang,
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': str(salt),
        'sign': str(sign),
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME',
    }

    res = requests.post(url=url, headers=headers, data=data).json()
    return res['translateResult'][0][0]['tgt']


def translator(content,to_lang):
    to_lang = to_lang[0:2]
    if to_lang == 'zh':
        to_lang = 'zh-CHS'
    result = send_request(content, to_lang)
    print(result)
    return result

if __name__ == '__main__':
    content = '你好啊，有道翻译'
    to_lang="sq-AL"
    to_lang=to_lang[0:2]
    if to_lang =='zh':
        to_lang='zh-CHS'
    result = send_request(content,to_lang)
    print(result)