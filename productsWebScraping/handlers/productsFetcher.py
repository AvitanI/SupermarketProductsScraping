import requests
from bs4 import BeautifulSoup

class ProductsFetcher:
    def __init__(self, chain_url):
        print('ProductsFetcher constructor', chain_url)
        self.chain_url = chain_url

    def get_parsed_html_by_chain_url(self, products_url):
        soup = None

        try:
            response = requests.get(products_url, verify=True)
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print('failed to get html response', str(e))

        return soup
