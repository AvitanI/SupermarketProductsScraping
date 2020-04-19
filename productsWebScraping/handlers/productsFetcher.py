import requests
from bs4 import BeautifulSoup

class ProductsFetcher:
    def __init__(self, chain_url):
        print('ProductsFetcher constructor', chain_url)
        self.chain_url = chain_url

    def get_parsed_html_by_chain_url(self, products_url):
        soup = None

        try:
            proxy_host = "proxy.crawlera.com"
            proxy_port = "8010"
            proxy_auth = ":"
            proxies = {
                "https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
                "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
            }
            response = requests.get(products_url, proxies=proxies, verify=False)
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print('failed to get html response', str(e))

        return soup
