from app import app
from productsWebScraping.handlers.shufersalProductsFetcher import ShufersalProductsFetcher
from productsWebScraping.handlers.ramiLeviProductsFetcher import RamiLeviProductsFetcher
from flask import jsonify
import requests
import dateutil.parser as parser
import traceback
import logging
import json

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

        logger.info('Product links: ' + json.dumps(product_links, default=lambda x: x.__dict__))
        # shufersal_instance = ShufersalProductsFetcher()
        # product_links = shufersal_instance.get_products_links()

        total_peroducts_per_store = []

        for product_link in product_links:

            products = ramiLevi_instance.get_products(product_link)

            total_peroducts_per_store.append({ 'storeID' : product_link.store_id, 'link' : product_link.linkForDownload, 'products' : len(products) })

            # result = dumps(products, ensure_ascii=False)

            for product in products:
                if 'PriceUpdateDate' in product:
                    product['PriceUpdateDate'] = parser.parse(product['PriceUpdateDate']).isoformat()

            payload = {
                'ChainID': 2,
                'StoreID': product_link.store_id,
                'Products': products
            }

            # prod: https://mysmartrefrigeratorwebapi.azurewebsites.net
            # dev: http://localhost:49847/api/Products/UpdateProducts

            r = requests.post('https://mysmartrefrigeratorwebapi.azurewebsites.net/api/Products/UpdateProducts', json=payload,verify=False)
            logger.info('Sent products to store: ' + product_link.store_id)

        # return result
        return jsonify(total_peroducts_per_store)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error('Failed to pull products: ' + json.dumps({ "error": str(e), "trace": tb }, default=lambda x: x.__dict__))
        return jsonify({ "error": str(e), "trace": tb })