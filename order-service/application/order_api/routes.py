# application/order_api/routes.py
from flask import jsonify, request, make_response
from sqlalchemy.orm import joinedload
from . import order_api_blueprint
from .. import db
from ..models import Order, OrderItem
from .api.UserClient import UserClient

import sys
import os
sys.path.insert(0, os.path.abspath('..'))


@order_api_blueprint.route('/api/orders', methods=['GET'])
def orders():
    items = []
    for row in Order.query.all():
        items.append(row.to_json())
    response = jsonify(items)
    return response


@order_api_blueprint.route('/api/order/add-item', methods=['POST'])
def order_add_item():
    api_key = request.headers.get('Authorization')
    response = UserClient.get_user(api_key)

    if not response:
        return make_response(jsonify({'message': 'Not logged in'}), 401)

    user = response['result']
    p_id = int(request.form['product_id'])
    qty = int(request.form['qty'])
    u_id = int(user['id'])

    known_order = Order.query.filter_by(user_id=u_id, is_open=1).first()

    if known_order is None:
        known_order = Order()
        known_order.is_open = True
        known_order.user_id = u_id

        order_item = OrderItem(p_id, qty)
        known_order.items.append(order_item)
    else:
        found = False

        for item in known_order.items:
            if item.product_id == p_id:
                found = True
                item.quantity += qty

        if found is False:
            order_item = OrderItem(p_id, qty)
            known_order.items.append(order_item)

    db.session.add(known_order)
    db.session.commit()
    response = jsonify({'result': known_order.to_json()})
    return response


@order_api_blueprint.route('/api/cart', methods=['GET'])
def cart():
    from frontend.application.frontend.api.ProductClient import ProductClient
    api_key = request.headers.get('Authorization')

    response = UserClient.get_user(api_key)

    if not response:
        return make_response(jsonify({'message': 'Not logged in'}), 401)

    user = response['result']
    open_order = Order.query.filter_by(user_id=user['id'], is_open=1).first()
    if open_order is None:
        response = jsonify({'result': {'items': []}})
    else:
        order = open_order.to_json()
        for item in order['items']:
            item['product'] = ProductClient.get_product_by_id(str(item['product']))[
                'result']
        response = jsonify({'result':  order})
    return response


@order_api_blueprint.route('/api/order', methods=['GET'])
def order():
    from frontend.application.frontend.api.ProductClient import ProductClient
    api_key = request.headers.get('Authorization')

    response = UserClient.get_user(api_key)

    if not response:
        return make_response(jsonify({'message': 'Not logged in'}), 401)

    user = response['result']
    open_order = Order.query.filter_by(user_id=user['id'], is_open=0).all()

    if open_order is None:
        response = jsonify({'result': {'items': []}})
    else:
        res = []
        for orders in open_order:
            order = orders.to_json()
            order['products'] = order['items'].copy()
            del order['items']
            for item in order['products']:
                item['product'] = ProductClient.get_product_by_id(str(item['product']))[
                    'result']
            res.append(order)
    response = jsonify({'result':  res})
    return response


@order_api_blueprint.route('/api/order/checkout', methods=['POST'])
def checkout():
    api_key = request.headers.get('Authorization')

    response = UserClient.get_user(api_key)

    if not response:
        return make_response(jsonify({'message': 'Not logged in'}), 401)

    user = response['result']

    order_model = Order.query.filter_by(user_id=user['id'], is_open=1).first()
    order_model.is_open = 0

    db.session.add(order_model)
    db.session.commit()

    response = jsonify({'result': order_model.to_json()})
    return response
