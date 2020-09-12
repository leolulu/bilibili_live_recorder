from flask import Flask, request
from qbittrent_api import QbittrentClient
from messenger import ijingniu_sender, server_chan_sender


app = Flask(__name__)


@app.route('/add_task', methods=['GET'])
def add_task():

    api = QbittrentClient()
    api.login()

    val = request.args.get('val')
    vals = val.split(',')
    if len(vals) == 2:
        result = api.add_torrent(vals[0], vals[1])
    else:
        result = api.add_torrent(vals[0])

    if result == 'success':
        server_chan_sender('添加torrent成功', vals[0])
    else:
        server_chan_sender('添加torrent失败', result)

    return '200'


if __name__ == '__main__':
    app.run(port=1125, host='0.0.0.0')
