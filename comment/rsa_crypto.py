import base64

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import os





# 生成私钥
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

# 从私钥中提取公钥
public_key = private_key.public_key()

# 加密数据
# message = b"This is a secret message"

def  encrypted(message):
    encrypted = public_key.encrypt(message,
                                   padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),
                                                label=None))
    return encrypted
def  decrypt(encrypted):
# 解密数据
    original_message = private_key.decrypt(encrypted, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                   algorithm=hashes.SHA256(), label=None))
    print("Decrypted message:", original_message)
    return original_message



def  str_to_encodedBytes(str):
    # 将字符串转换为字节数组
    encoded_data = base64.b64encode(str.encode('utf-8'))
    return encoded_data
def  encodedBytes_to_str(base64_data):
    # base64编码的数据
    # base64_data = b'SGVsbG8gd29ybGQh'  # 注意，这是一个bytes类型的字面量
    # 解码base64数据
    decoded_bytes = base64.b64decode(base64_data)
    # 将解码后的bytes转换为字符串
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string


if __name__ == '__main__':
    accessKeyId = "kjdklasjdklajdaksljdaskljdsakljaskldj"
    accessKeySecret = "lksajdklasjdkasjdklasjdklasjdklasjdklasmdkasmdkasmsakm"
    accessKeyId=str_to_encodedBytes(accessKeyId)
    encrypted= encrypted(accessKeyId)
    print(encrypted)
    message=decrypt(encrypted)
    message= encodedBytes_to_str(message)
    print(message)