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
    key = b"efa3304d9802c623675325f24c0de717"
    data = b"3052020100044b30490201000204413e3b6802032df7950204db5d06af020465870cce042437316662343732372d353338352d343937372d386533342d34386665616436333161613902040114000f0201000400"
    mi = aes_encode(data, key)
    print("加密值：", mi)
    print("解密值：", aes_decode(data, key))

