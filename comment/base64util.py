import base64
from Crypto.Cipher import AES


def aes_decode(data, key):
    try:
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
        decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf8'))).decode("utf8")  # 解密
        decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
    except Exception as e:
        pass
    return decrypted_text


# 加密
def aes_encode(data, key):
    while len(data) % 16 != 0:  # 补足字符串长度为16的倍数
        data += (16 - len(data) % 16) * chr(16 - len(data) % 16)
        data = str.encode(data)
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
    return str(base64.encodebytes(aes.encrypt(data)), encoding='utf8').replace('\n', '')  # 加密






if __name__ == '__main__':
    # key = b"efa3304d9802c623675325f24c0de717"
    # data = b"3052020100044b30490201000204413e3b6802032df7950204db5d06af020465870cce042437316662343732372d353338352d343937372d386533342d34386665616436333161613902040114000f0201000400"
    # mi = aes_encode(data, key)
    # print("加密值：", mi)
    # print("解密值：", aes_decode(data, key))
    base=b'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'
    file_path="F:\\test_voice\\test.ts"
    data = base64.b64decode(base)
    with open(file_path, 'wb') as f:
        f.write(data)
