from messenger import ijingniu_sender
from time import sleep


for _ in range(20):
    sleep(3)
    ijingniu_sender(
        "44重启了！！！",
        "可能由于系统更新等原因，反正机器重启了，快去手动启动录播姬！！！"
    )
