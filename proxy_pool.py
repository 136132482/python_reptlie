import os
import threading

def  start_proxy_schedule():
    # sys.exit()
    # time.sleep(5)
    cmd="python  F:\\python_workspace\\proxy_pool-master\\proxyPool.py schedule"
    os.system(cmd)

def start_proxy_server():
    cmd1="python F:\\python_workspace\\proxy_pool-master\\proxyPool.py server"
    os.system(cmd1)



thread = threading.Thread(target=start_proxy_server)
thread.start()
thread1 = threading.Thread(target=start_proxy_schedule)
thread1.start()