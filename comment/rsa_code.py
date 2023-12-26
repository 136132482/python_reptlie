import base64

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.PublicKey import RSA

from comment import rsa_crypto

#用于密文长度太长的问题 由于RSA的特性，一个1024位的密钥只能加密117位字节数据，当数据量超过117位字节的时候，程序就会抛出异常

public_key = "conf/public.pem"
private_key = "conf/private.pem"


class RsaCode():
    def encrypt(self, msg):
        # msg = msg.encode('utf-8')
        rsa_public_key = open(public_key).read()
        rsakey = RSA.importKey(rsa_public_key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(msg))
        return cipher_text

    def decrypt(self, cipher_text):
        rsa_private_key = open(private_key).read()
        rsakey = RSA.importKey(rsa_private_key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        random_generator = Random.new().read
        text = cipher.decrypt(base64.b64decode(cipher_text), random_generator)
        return text.decode('utf8')

    def long_encrypt(self, msg):
        # msg = msg.encode('utf-8')
        length = len(msg)
        default_length = 117
        # 公钥加密
        rsa_public_key = open(public_key).read()
        pubobj = Cipher_pkcs1_v1_5.new(RSA.importKey(rsa_public_key))
        # 长度不用分段
        if length < default_length:
            return base64.b64encode(pubobj.encrypt(msg))
        # 需要分段
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(pubobj.encrypt(msg[offset:offset + default_length]))
            else:
                res.append(pubobj.encrypt(msg[offset:]))
            offset += default_length
        byte_data = b''.join(res)
        return base64.b64encode(byte_data)

    def long_decrypt(self, msg):
        msg = base64.b64decode(msg)
        length = len(msg)
        default_length = 128
        # 私钥解密
        rsa_private_key = open(private_key).read()
        priobj = Cipher_pkcs1_v1_5.new(RSA.importKey(rsa_private_key))
        # 长度不用分段
        if length < default_length:
            return b''.join(priobj.decrypt(msg, b'xyz'))
        # 需要分段
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(priobj.decrypt(msg[offset:offset + default_length], b'xyz'))
            else:
                res.append(priobj.decrypt(msg[offset:], b'xyz'))
            offset += default_length
        return  b''.join(res)



    def   create_rsa(self):
        # 伪随机数生成器
        random_gen = Random.new().read
        # 生成秘钥对实例对象：1024是秘钥的长度
        rsa = RSA.generate(1024, random_gen)
        # 获取公钥，保存到文件
        private_pem = rsa.exportKey()
        with open('conf/private.pem', 'wb') as f:
            f.write(private_pem)

        # 获取私钥保存到文件
        public_pem = rsa.publickey().exportKey()
        with open('conf/public.pem', 'wb') as f:
            f.write(public_pem)


    def encrypt_file(self,file_path):
        """使用RSA算法加密文件
        参数：
        file_path: 需要加密的文件路径
        public_key_file: 公钥文件路径
        返回值：
        无
        """
        # 读取文件内容
        with open(file_path, "rb") as file:
            file_content = file.read()
        # 读取公钥
        # 计算需要添加的等号数
        # missing_padding = len(file_content) % 4
        # if missing_padding:
        #     file_content += b'=' * (4 - missing_padding)
        # print(file_content)
        text=self.long_encrypt(file_content)
        print(text)
        # 加密文件内容
        # 将加密后的内容写入文件
        with open(file_path, "wb") as file:
            file.write(text)

    def decrypt_file(self,file_path):
        oss_key={}
        # 读取文件内容
        with open(file_path, "rb") as file:
            encrypted_content = file.read()
            # 读取私钥
            # 解密文件内容
        text=self.long_decrypt(encrypted_content)
        text=text.decode('utf8')
        list=text.split("\n")
        for i in range(len(list)):
             name=list[i].split(":")
             if len(name)>1:
                 oss_key[name[0].strip()]=name[1].strip()
        return oss_key
        # 将解密后的内容写入文件
        # with open(file_path, "wb") as file:
        #     file.write(text)

if __name__ == '__main__':
    # message = '''{"userId":"2088002933729603","transLongitude":"55.755831","transLatitude":"37.617673","merNo":"M000178103","terminalNo":"mini202007030908154720106107","terminalLongitude":"65.755831","terminalLatitude":"77.617673","createTime":"1514561699","tradeType":"WX","orderId":"202207102377965187OR012471381501"}'''
    test = RsaCode()
    # create_rsa()
    # res_en = test.long_encrypt(message)
    # print('res_en', res_en)
    # res_de = test.long_decrypt(res_en)
    # print('res_de', res_de)
    # res_ren = b'sFXiDF+vDIKoIcOg/h9awIqYi0bOHAMXgmeYH4SBKolNXXUuYJAZhJpOh1MvIDxddxE5vvnHF9wUHbMPSB6wLfh+q+u5r6yBY1a5WP3mGETCxRDxThSxhAzKWzuSL2cwK3Teqz6cfL3qfXIEZp6s4iUeKv4HbBbGaVwyoLcrbfKCbBjNb+e4B3xHqesoab89icPT03N8KTqOll44gTMAMhiB13ABmp0EzEVu0ZYsqET73vyhh2hyPQQVb8ap9cKyiilNHVU42I4ET+5mBL31yOZOpC34ESIHcQKKgFhAndsHlUCwavRdZyobanTuYI7Pn0fEBnNqF5wdpVAp8evie82Lu0E52bmok8Ys3mty91yLvHmWkro7yqQz7iSVf40/QaB5Qjyu7jwucJGlBvF+Pc2/cgLvlocks7y+dE72wwEmWx3GgZBNS7OeQl6a34/OU0Uv34klxe94T8+c6/Q7roXSzTS3W6/EZjefIryWc+DUAqjkQYwhWo+ObT88Zq2X'
    # res_den = test.long_decrypt(res_ren)
    # print('res_den', res_den)
    # test.encrypt_file("F:\python_workspace\python_replite\comment\crypto_config.yaml")
    oss_key=test.decrypt_file("F:\python_workspace\python_replite\comment\crypto_config.yaml")
