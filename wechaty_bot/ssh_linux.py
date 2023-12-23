from time import sleep

import yaml
import paramiko
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s <%(funcName)s> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

log = logging.getLogger(__name__)

with open('ssh_linux.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 访问配置选项
host = config['ssh_linux']['host']
port = config['ssh_linux']['port']
user = config['ssh_linux']['username']
password = config['ssh_linux']['password']

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加主机名及主机密钥到本地HostKeys对象，并保存
ssh.connect(host, port, user, password)  # 使用用户名和密码进行连接

# cmd="sh /usr/local/wechaty/wechaty.sh"
cmd="docker restart wechaty"
stdin, stdout, stderr = ssh.exec_command(cmd) # 执行命令
sleep(1)
ssh.close()
print(stdout)