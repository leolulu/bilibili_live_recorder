import requests
from urllib.parse import urljoin
import json


class QbittrentClient:
    def __init__(self):
        self.set_url_type('remote')
        self.headers = {'Referer': self.base_url}
        self.log = ''

    def _print(self, *args):
        print(*args)
        for i in args:
            self.log += str(i) + ' '
        self.log += '\n'

    def sent_to_server_chan(self):
        url = 'https://sctapi.ftqq.com/SCT1373TjRduEhiDYMtaoL6egD1z0d5u.send'
        data = {
            'title': 'torrent恢复',
            'desp': self.log.replace('\n', '\n\n')
        }
        requests.post(url, data=data)

    def set_url_type(self, type: str):
        if type not in ['local', 'remote']:
            raise UserWarning("urltype只能为'local'或'remote'...")
        elif type == 'local':
            self.base_url = 'http://127.0.0.1:8484'
        elif type == 'remote':
            self.base_url = 'http://132.232.0.240:20004'

    def login(self):
        params = {'username': 'btbtbt', 'password': 'btbtbt'}
        url = urljoin(self.base_url, '/api/v2/auth/login')
        r = requests.get(url, params=params)
        if r.status_code != 200:
            self._print('登录失败，返回码：{}...'.format(r.status_code))
            return None
        self._print('登录成功...')
        self.cookies = dict(r.cookies)
        self._print('cookie为：', self.cookies)

    def logout(self):
        url = urljoin(self.base_url, '/api/v2/auth/logout')
        r = requests.get(url, cookies=self.cookies, headers=self.headers)
        if r.status_code == 200:
            self._print('成功登出了...')

    def get_torrent_info(self):
        url = urljoin(self.base_url, '/api/v2/torrents/info')
        if self.cookies:
            r = requests.get(url, cookies=self.cookies, headers=self.headers)
            if r.status_code != 200:
                self._print('获取torrent失败，返回码：{}...'.format(r.status_code))
                return None
            return json.loads(r.content)

    def get_error_torrent(self):
        torrent_list = self.get_torrent_info()
        error_torrents = [
            {
                'hash': i['hash'],
                'name':i['name'],
                'state':i['state'],
                'progress':'{:.1%}'.format(i['progress'])
            }
            for i in torrent_list if i['state'] == 'error'
        ]
        return error_torrents

    def resume_torrent(self):
        url = urljoin(self.base_url, '/api/v2/torrents/resume')
        if self.cookies:
            error_torrents = self.get_error_torrent()
            for error_torrent in error_torrents:
                params = {'hashes': error_torrent['hash']}
                r = requests.get(url, cookies=self.cookies, headers=self.headers, params=params)
                if r.status_code != 200:
                    self._print('torrent失败，返回码：{}...'.format(r.status_code))
                elif r.status_code == 200:
                    self._print('恢复成功：{}'.format(error_torrent['name'],))
            if error_torrents:
                return 'not empty'


if __name__ == "__main__":
    api = QbittrentClient()
    api.login()
    has_error = api.resume_torrent()
    api.logout()
    if has_error:
        api.sent_to_server_chan()
