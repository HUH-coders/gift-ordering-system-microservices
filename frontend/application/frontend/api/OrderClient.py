# application/frontend/api/OrderClient.py
from flask import session
import requests


class OrderClient:
    @staticmethod
    def get_order():
        headers = {
            'Authorization': 'Basic ' + session['user_api_key']
        }
        url = 'http://192.168.0.104:5003/api/order'
        response = requests.request(method="GET", url=url, headers=headers)
        order = {}
        try:
            order = response.json()
        except:
            print("Order not found!")
        return order

    @staticmethod
    def get_cart():
        headers = {
            'Authorization': 'Basic ' + session['user_api_key']
        }
        url = 'http://192.168.0.104:5003/api/cart'
        response = requests.request(method="GET", url=url, headers=headers)
        cart_items = response.json()
        print(cart_items)
        return cart_items

    @staticmethod
    def post_add_to_cart(product_id, qty=1):
        payload = {
            'product_id': product_id,
            'qty': qty
        }
        url = 'http://192.168.0.104:5003/api/order/add-item'

        headers = {
            'Authorization': 'Basic ' + session['user_api_key']
        }
        response = requests.request(
            "POST", url=url, data=payload, headers=headers)
        if response:
            order = response.json()
            return order

    @staticmethod
    def post_checkout():
        url = 'http://192.168.0.104:5003/api/order/checkout'

        headers = {
            'Authorization': 'Basic ' + session['user_api_key']
        }
        response = requests.request("POST", url=url, headers=headers)
        order = response.json()
        return order

    @staticmethod
    def get_order_from_session():
        default_order = {
            'items': {},
            'total': 0,
        }
        return session.get('order', default_order)
