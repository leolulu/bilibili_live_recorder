import requests
import sys


def server_chan_sender(title: str, content: str) -> str:
    url = 'https://sctapi.ftqq.com/SCT1373TjRduEhiDYMtaoL6egD1z0d5u.send'
    data = {
        'title': title,
        'desp': content
    }
    r = requests.post(url, data=data)
    if r.status_code == 200:
        return 'ok'
    else:
        return str(r.status_code)


def ijingniu_sender(title: str, content: str) -> str:
    url = 'http://push.ijingniu.cn/send'
    data = {
        'key': 'd21579c4c39f4e51bedf606ef4d3e07d',
        'head': title,
        'body': content
    }
    r = requests.post(url, data=data)
    if r.status_code == 200:
        return 'ok'
    else:
        return str(r.status_code)


# def ijingniu_callback():
#     pass

if __name__ == "__main__":
    if len(sys.argv) == 3:
        ijingniu_sender(sys.argv[1], sys.argv[2])
