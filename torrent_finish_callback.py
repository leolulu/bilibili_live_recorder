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


def gen_at_job(name, category, org_folder_path) -> str:
    target_folder_path = '/mnt/0DB8/share已完成/'
    recycle_bin_path = '/mnt/0DB8/share已完成/回收站/'
    source_path = os.path.join(org_folder_path, name)
    target_name = '{}==》{}'.format(category, name)
    target_path = os.path.join(target_folder_path, target_name)
    recycle_bin_target_path = os.path.join(recycle_bin_path, target_name)
    message = []

    # command = r'mv \"{}\" \"{}\"'.format(source_path, recycle_bin_target_path) # 原本是移动
    command = r'rm -r \"{}\"'.format(source_path)  # 现在改成删除
    at_command = 'echo "{}" | at now +14 days'.format(command)
    p = subprocess.Popen(at_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    message.append(f'at执行信息:\n{p.stderr.read().decode()}')

    command = 'cp -r -v "{}" "{}"'.format(source_path, target_path)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    message.append(f'即时复制执行信息:\n{p.stdout.read().decode()}')

    return '\n'.join(message).replace("'", ' ')


if __name__ == '__main__':
    torrent_finish_callback(sys.argv[1])
