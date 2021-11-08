# application/frontend/api/ProductClient.py
import requests


class ProductClient:

    @staticmethod
    def get_products():
        r = requests.get('http://192.168.0.108:5002/api/products')
        try:
            products = r.json()
        except:
            products = {
                "results": []
            }

        return products

    @staticmethod
    def get_product(slug):
        response = requests.request(
            method="GET", url='http://192.168.0.108:5002/api/product/' + slug)
        product = response.json()
        return product

    @staticmethod
    def get_product_by_id(id):
        response = requests.request(
            method="GET", url='http://192.168.0.108:5002/api/product/id/' + id)
        product = response.json()
        return product
