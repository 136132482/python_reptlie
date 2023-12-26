import base64
import rsa
import os
import rsa_crypto
def encrypt_file(file_path, public_key_file):
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
    with open(public_key_file, "rb") as key_file:
        public_key = rsa.PublicKey.load_pkcs1(key_file.read())
    # 加密文件内容
    encrypted_content = rsa.encrypt(file_content, public_key)
    # 将加密后的内容写入文件
    with open(file_path, "wb") as file:
        file.write(encrypted_content)


def decrypt_file(file_path, private_key_file, password):
    """使用RSA算法解密文件

    参数：
    file_path: 需要解密的文件路径
    private_key_file: 私钥文件路径
    password: 私钥文件密码

    返回值：
    无
    """
    # 读取文件内容
    with open(file_path, "rb") as file:
        encrypted_content = file.read()
    # 读取私钥
    with open(private_key_file, "rb") as key_file:
        private_key = rsa.PrivateKey.load_pkcs1(key_file.read(), password)
    # 解密文件内容
    file_content = rsa.decrypt(encrypted_content, private_key)
    # 将解密后的内容写入文件
    with open(file_path, "wb") as file:
        file.write(file_content)


# rsa加密
def rsa_encrypt(value):
    # 生成公钥、私钥
    pub_key, priv_key = rsa.newkeys(256)  # 88时能够加密的字节为0，后续每增加8，代表增加一个字节
    # 明文编码格式
    content = value.encode('utf-8')
    # 明文加密
    crypto = rsa.encrypt(content, pub_key)
    # 返回密文和私钥
    return (crypto, priv_key)


# rsa解密
def rsa_decrypt(crypto, pk):
    # 私钥解密
    content = rsa.decrypt(crypto, pk)
    con = content.decode('utf-8')
    return con




# if __name__ == '__main__':
#     v = '要加密的数据'
#     crypto, pk = rsa_encrypt(v)
#     print('加密后密文：%s' % crypto)
#     content = rsa_decrypt(crypto, pk)
#     print('解密后明文：%s' % content)

if __name__ == '__main__':
    pub_key_obj, priv_key_obj = rsa.newkeys(256)
    pub_key_str = pub_key_obj.save_pkcs1()
    # pub_key_code = base64.b64encode(pub_key_str)
    # pub_key_str= rsa_crypto.encodedBytes_to_str(pub_key_code)


    priv_key_str = priv_key_obj.save_pkcs1()
    # priv_key_code = base64.b64encode(priv_key_str)
    # priv_key_str= rsa_crypto.encodedBytes_to_str(priv_key_code)

    # print(pub_key_str)
    # print(priv_key_str)
    #
    #
    rsa_decrypt_path="F:\\python_workspace\\python_replite\\comment\\crypto_config.yaml"
    public_key="F:\\rsa\\private.txt"
    private_key="F:\\rsa\\public.txt"

    # with open(public_key, "wb") as file:
    #     file.write(pub_key_str)
    #
    # with open(private_key, "wb") as file:
    #     file.write(priv_key_str)

    encrypt_file(rsa_decrypt_path,public_key)
