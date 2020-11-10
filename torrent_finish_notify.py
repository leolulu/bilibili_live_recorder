from qbittrent_api import QbittrentClient

def get_torrent_info(_hash):
    api = QbittrentClient()
    api.login()
    api.get_torrent_info(_hash)

    message = ''
    

    api.logout()