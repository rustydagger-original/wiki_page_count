import requests

class DownLoader(object):
    def __init__(self, logger, proxy=None):
        self.custom_proxy = proxy
        self.logger = logger

    def download(self, url):
        if self.custom_proxy:
            response = requests.get(url, proxies=self.custom_proxy, stream=True)
        else:
            response = requests.get(url, stream=True)

        if response.status_code == 404:
            self.logger.error("{0} Is Not Found".format(url))
            return None

        return response.content