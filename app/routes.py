from app import app
from productsWebScraping.handlers.shufersalProductsFetcher import ShufersalProductsFetcher
from productsWebScraping.handlers.ramiLeviProductsFetcher import RamiLeviProductsFetcher
from flask import jsonify
import requests
import dateutil.parser as parser

@app.route('/')
def koko():
    return "popo"

@app.route('/getProducts')
def get_products():
    try:
        from bson.json_util import dumps

        ramiLevi_instance = RamiLeviProductsFetcher()
        product_links = ramiLevi_instance.get_products_links()

        # shufersal_instance = ShufersalProductsFetcher()
        # product_links = shufersal_instance.get_products_links()


        for product_link in product_links:

            products = ramiLevi_instance.get_products(product_link)

            # result = dumps(products, ensure_ascii=False)

            for product in products:
                if 'PriceUpdateDate' in product:
                    product['PriceUpdateDate'] = parser.parse(product['PriceUpdateDate']).isoformat()

            json = {
                'ChainID': 2,
                'StoreID': product_link.store_id,
                'Products': products
            }

            r = requests.post('http://localhost:49847/api/Products/UpdateProducts', json=json,verify=False)

        # return result
        return 'OK'
    except Exception as e:
        return jsonify({ "error": str(e) })