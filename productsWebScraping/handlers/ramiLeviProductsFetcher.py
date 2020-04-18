from productsWebScraping.handlers.productsFetcher import ProductsFetcher
from productsWebScraping.models.productDownload import ProductDownload
import urllib.request
from io import BytesIO
import gzip
from bs4 import BeautifulSoup, Tag
# import mechanize
# import cookiejar
import requests
import re

# Temp store ids
haifa_store_ids = ["019", "057"]

# searching categories
search_categories = {
     'all' : 0 ,
     'prices' : 1 ,
     'pricesFull' : 2 ,
     'promos' : 3 ,
     'promosFull' : 4 ,
     'stores' : 5
}

# Prices web URL
RAMILEVI_URL = 'https://url.retail.publishedprices.co.il/file'
DOWNLOAD_URL = 'https://url.retail.publishedprices.co.il/file/d/'

class RamiLeviProductsFetcher(ProductsFetcher):
    def __init__(self):
        print(__name__ + ' constructor')
        super(RamiLeviProductsFetcher, self).__init__(RAMILEVI_URL)

        self.session = requests.Session()

    def get_products_links(self):
        # Get chain html as Beautiful Soup
        parsed_html = self.get_parsed_html_by_chain_url(RAMILEVI_URL)

        files = self.koko(parsed_html)

        products_to_download = []

        # Find all links for product downloading
        for file in files:
            file_name = file['fname']

            match = re.search('^priceFull\d+\-(?P<store_id>\d+)\-\d+\.gz$', file_name, flags=re.IGNORECASE)

            if match is None:
                continue

            store_id = match.group('store_id')

            if store_id in haifa_store_ids:
                if any(p.store_id == store_id for p in products_to_download):
                    continue

                products_link_to_download = DOWNLOAD_URL + file_name
                file_name = file_name
                product_to_download = ProductDownload(store_id, file_name, products_link_to_download)
                products_to_download.append(product_to_download)

        return products_to_download

    def koko(self, parsed_html):
        # Find login form
        login_form = parsed_html.find('form', id='login-form')

        # The action submit to
        action = login_form.get('action')

        # Get all named inputs from login form
        form_named_inputs = login_form.find_all('input', { 'name': True })

        # Get form inputs as key value pair
        key_value_inputs = { input['name']: input.get('value', '') for input in form_named_inputs }

        key_value_inputs['username'] = 'RamiLevi'

        # first = session.get('https://url.retail.publishedprices.co.il', verify=False)
        login = self.session.post('https://url.retail.publishedprices.co.il' + action, headers={ 'Content-Type': 'application/x-www-form-urlencoded' }, data=key_value_inputs, verify=False)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'sEcho': '1',
            'iColumns': '5',
            'sColumns':',, , ,',
            'iDisplayStart': '0',
            'iDisplayLength': '100000',
            'mDataProp_0': 'fname',
            'sSearch_0': '',
            'bRegex_0':'false',
            'bSearchable_0': 'true',
            'bSortable_0': 'true',
            'mDataProp_1': 'type',
            'sSearch_1':'',
            'bRegex_1':'false',
            'bSearchable_1': 'true',
            'bSortable_1': 'false',
            'mDataProp_2': 'size',
            'sSearch_2':'',
            'bRegex_2':'false',
            'bSearchable_2': 'true',
            'bSortable_2': 'true',
            'mDataProp_3': 'ftime',
            'sSearch_3':'',
            'bRegex_3':'false',
            'bSearchable_3': 'true',
            'bSortable_3': 'true',
            'mDataProp_4':'',
            'sSearch_4':'',
            'bRegex_4': 'false',
            'bSearchable_4': 'true',
            'bSortable_4': 'false',
            'sSearch':'',
            'bRegex':'false',
            'iSortingCols': '0',
            'cd': '/',
        }

        files = self.session.post('https://url.retail.publishedprices.co.il/file/ajax_dir', headers=headers, data=payload, verify=False)
        res = files.json()
        return res['aaData']

    def get_products(self, product_link):
        try:
            ress = self.session.get(product_link.linkForDownload)
            cont = ress.content
            # response = urllib.request.urlopen(product_link.linkForDownload)
            # compressed_file = BytesIO(response.read())
            compressed_file = BytesIO(cont)
            decompressed_file = gzip.GzipFile(fileobj=compressed_file)
            y = decompressed_file.read().decode("utf-8")
            soup = BeautifulSoup(y, "xml")
            all_items_codes = soup.find_all("ItemCode")

            arr = []

            for item_code in all_items_codes:
                # if item_code.text != product_id:
                #     continue

                dic = {}

                for children in item_code.parent():
                    dic[children.name] = children.text

                arr.append(dic)

            # print(dic)

            return arr
        except Exception as e:
            print('failed to download', str(e))

            return []