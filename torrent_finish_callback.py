import os
import re
import shutil
import subprocess
import sys
import traceback

from copy_util import recursive_search_source_folder
from messenger import ijingniu_sender
from qbittrent_api import QbittrentClient
from torrent_finish_notify import torrent_finish_notify


def torrent_finish_callback(_hash):
    api = QbittrentClient()
    api.login()
    torrent_list = api.get_torrent_list(_hash)

    name = torrent_list[0]['name']
    category = torrent_list[0]['category']
    content_path = torrent_list[0]['content_path']
    message = None

    title = "下载完成"
    try:
        if re.search(r"^\d+$", category) or (category in ['hacg', 'movie', 'anime', 'game', 'horse', 'porn', 'hanime']):
            message = gen_at_job(name, category, content_path)
    except Exception as e:
        message = traceback.format_exc()
        title = "下载完成但复制失败"

    api.logout()

    ijingniu_sender(title, torrent_finish_notify(_hash, message))


def gen_at_job(name, category, source_path) -> str:
    if os.path.isfile(source_path):
        source_path = os.path.dirname(source_path)
    target_folder_path = '/mnt/hdd/qbitDownload/finish'
    recycle_bin_path = '/mnt/0DB8/share已完成/回收站/'
    tmp_path = '/mnt/hdd/tmp'
    target_name = '{}==》{}'.format(category, name)
    tmp_path = os.path.join(tmp_path, target_name)
    target_path = os.path.join(target_folder_path, target_name)
    recycle_bin_target_path = os.path.join(recycle_bin_path, target_name)
    message = []

    # command = r'mv \"{}\" \"{}\"'.format(source_path, recycle_bin_target_path) # 原本是移动
    # command = r'rm -r \"{}\"'.format(source_path)  # 现在改成删除
    #at_command = 'echo "{}" | at now +14 days'.format(command)
    #p = subprocess.Popen(at_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # p.wait()
    # message.append(f'at执行信息:\n{p.stderr.read().decode()}')

    # command = 'cp -r -v "{}" "{}"'.format(source_path, target_path)
    # p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # p.wait()
    # message.append(f'即时复制执行信息:\n{p.stdout.read().decode()}\n{p.stderr.read().decode()}')

    os.mkdir(tmp_path)
    cp_msg = recursive_search_source_folder(source_path, tmp_path)
    shutil.move(tmp_path, target_folder_path)
    message.append(f'即时复制执行信息:\n')
    message += cp_msg
    try:
        subprocess.call(f'chmod -R 777 "{target_path}"', shell=True)
    except Exception as e:
        message.append(f'赋权失败了:\n')
        message += str(e)

    return '\n'.join(message).replace("'", ' ')


if __name__ == '__main__':
    torrent_finish_callback(sys.argv[1])
