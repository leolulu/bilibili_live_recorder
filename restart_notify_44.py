from messenger import ijingniu_sender
from time import sleep


for i in range(20):
    i = i + 1
    ijingniu_sender(
        f"【{i}】44重启了！！！",
        f"【{i}】可能由于系统更新等原因，反正机器重启了，快去手动启动录播姬！！！"
    )
    sleep(3)
