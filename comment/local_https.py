# coding=utf-8

import http.server
import ssl


def https_web_server():
    """
    https服务器
    :return:
    """
    server_ip = '127.0.0.1'
    # 这里port不要写成字符串，我刚开始给成字符串，报错搞了好一会
    server_port = 8001
    server_address = (server_ip, server_port)
    # 生成证书步骤：
    # openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
    server_cert = "F:\\ssl\\cert.pem"
    server_key = "F:\\ssl\\key.pem"
    DIRECTORY = 'F:\\test_voice'
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        server_side=True,
        certfile=server_cert,
        keyfile=server_key,
        ssl_version=ssl.PROTOCOL_TLS)

    print("Server HTTPS on " + server_ip + " port " + str(server_port) + " (https://" + server_ip + ":" + str(server_port) + ") ... ")
    httpd.serve_forever()


if __name__ == '__main__':
    https_web_server()


