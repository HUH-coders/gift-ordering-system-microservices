# application/frontend/api/ProductClient.py
import requests


class ProductClient:

    @staticmethod
    def get_products():
        r = requests.get('http://192.168.0.101:5002/api/products')
        products = r.json()
        return products

    @staticmethod
    def get_product(slug):
        response = requests.request(method="GET", url='http://192.168.0.101:5002/api/product/' + slug)
        product = response.json()
        return product
