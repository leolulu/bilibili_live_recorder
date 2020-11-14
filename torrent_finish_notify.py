import os
import arrow
from datetime import timedelta
import sys

from messenger import ijingniu_sender
from qbittrent_api import QbittrentClient
from generic_util import get_time_diff


def torrent_finish_notify(_hash):
    api = QbittrentClient()
    api.login()
    torrent_list = api.get_torrent_list(_hash)
    torrent_info = api.get_torrent_info(_hash)

    message = ''

    name = torrent_list[0]['name']
    category = torrent_list[0]['category']
    # save_path = os.path.basename(save_path)
    message += f"任务分类:\n[{category}]\n\n任务名称:\n{name}\n\n"

    creation_date = torrent_info['creation_date']
    creation_date = arrow.get(creation_date, tzinfo='local')
    creation_date_formated = creation_date.format('YYYY-MM-DD HH:mm:ss')
    creation_date_diff = get_time_diff(creation_date)
    message += f"添加于:\n{creation_date_formated}（{creation_date_diff}）\n\n"

    total_size = torrent_info['total_size']
    total_size = round(total_size/(1024*1024*1024), 2)
    message += f'总大小:\n{total_size}GB\n\n'

    time_elapsed = torrent_info['time_elapsed']
    time_elapsed_diff = get_time_diff(arrow.now()-timedelta(seconds=time_elapsed))
    message += f'总耗时:\n{time_elapsed_diff}'

    api.logout()

    return message


if __name__ == "__main__":
    ijingniu_sender("下载完成", torrent_finish_notify(sys.argv[1]))
