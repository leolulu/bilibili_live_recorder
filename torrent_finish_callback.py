import os
import re
import subprocess
import sys

from messenger import ijingniu_sender
from qbittrent_api import QbittrentClient
from torrent_finish_notify import torrent_finish_notify


def torrent_finish_callback(_hash):
    api = QbittrentClient()
    api.login()
    torrent_list = api.get_torrent_list(_hash)

    name = torrent_list[0]['name']
    category = torrent_list[0]['category']
    save_path = torrent_list[0]['save_path']
    message = None

    if re.search(r"^\d+$", category) or (category in ['hacg']):
        message = gen_at_job(name, category, save_path)

    api.logout()

    ijingniu_sender("下载完成", torrent_finish_notify(_hash, message))


def gen_at_job(name, category, org_folder_path):
    target_folder_path = '/mnt/0DB8/share已完成/'
    target_name = '{}---{}'.format(category, name)
    target_path = os.path.join(target_folder_path, target_name)
    source_path = os.path.join(org_folder_path, name)

    command = 'mv "{}" "{}"'.format(source_path, target_path)
    at_command = 'echo "{}" | at now +7 days'.format(command)

    p = subprocess.Popen(at_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    message = f'at执行信息:\n{p.stderr.read().decode()}'
    return message


if __name__ == '__main__':
    torrent_finish_callback(sys.argv[1])
