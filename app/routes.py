from app import app
from productsWebScraping.handlers.shufersalProductsFetcher import ShufersalProductsFetcher
from productsWebScraping.handlers.ramiLeviProductsFetcher import RamiLeviProductsFetcher
from flask import jsonify
import requests
import dateutil.parser as parser
import traceback
import logging

@app.route('/')
def home():
    return "Product Scraping API"

@app.route('/getProducts')
def get_products():
    logger = logging.getLogger()

    try:
        # from bson.json_util import dumps

        ramiLevi_instance = RamiLeviProductsFetcher()
        product_links = ramiLevi_instance.get_products_links()

        logger.info('Product links: ' + jsonify(product_links))

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

            # prod: https://mysmartrefrigeratorwebapi.azurewebsites.net
            # dev: http://localhost:49847/api/Products/UpdateProducts

            r = requests.post('https://mysmartrefrigeratorwebapi.azurewebsites.net/api/Products/UpdateProducts', json=json,verify=False)
            logger.info('Sent products to store: ' + product_link.store_id)

        # return result
        return 'OK'
    except Exception as e:
        tb = traceback.format_exc()
        logger.error('Failed to pull products: ' + jsonify({ "error": str(e), "trace": tb })
        return jsonify({ "error": str(e), "trace": tb })