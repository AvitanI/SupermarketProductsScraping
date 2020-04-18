from productsWebScraping.handlers.productsFetcher import ProductsFetcher
from productsWebScraping.models.productDownload import ProductDownload
import urllib.request
from io import BytesIO
import gzip
from bs4 import BeautifulSoup, Tag

# Temp store ids
haifa_store_ids = ["212", "302", "306", "4", "17", "19", "33", "38", "159", "312", "314", "327", "330", "333", "336", "353", "359", "368", "387", "388", "650", "659", "673", "328", "143", "186"]

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
SHUFERSAL_URL = 'http://prices.shufersal.co.il/FileObject/UpdateCategory'

class ShufersalProductsFetcher(ProductsFetcher):
    def __init__(self):
        print(__name__ + ' constructor')
        super(ShufersalProductsFetcher, self).__init__(SHUFERSAL_URL)

    def get_products_links(self):
        product_links = []

        for store_id in haifa_store_ids:
            product_link = self.__get_products_link_by_store_id(store_id)

            if not product_link:
                continue

            product_links.append(product_link)

        return product_links

    def __get_products_link_by_store_id(self, store_id):
        query_string = '?catID={0}&storeId={1}'.format(search_categories['pricesFull'], store_id)

        # Get chain html as Beautiful Soup
        parsed_html = self.get_parsed_html_by_chain_url(SHUFERSAL_URL + query_string)

        # Find all a tags
        all_a_tags = parsed_html.findAll('a')

        # Find all links for product downloading
        for tag in all_a_tags:
            if tag.text != 'לחץ להורדה':
                continue

            products_link_to_download = tag.attrs['href']
            file_name = tag.parent.find_next_siblings()[5].text

            productToDownload = ProductDownload(store_id, file_name, products_link_to_download)

            return productToDownload

        return ''

    def get_products(self, product_link):
        try:
            response = urllib.request.urlopen(product_link.linkForDownload)
            compressed_file = BytesIO(response.read())
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