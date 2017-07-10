from flask import jsonify, request, url_for
from sqlalchemy import func
from . import api
from .. import db
from ..models import User, Cake, Order 
from datetime import datetime

@api.route('/orders')
def get_orders():
  orders = Order.query.all()
  ords = [];
  for order in orders:
    user = order.user.to_json()
    cake = order.cake.to_json()
    ords.append(order.to_json(user, cake))
  return jsonify({'orders' : ords})

@api.route('/orders/status/<int:statusNum>')
def get_orders_statusNum(statusNum):
  print statusNum
  orders = Order.query.filter_by(status=statusNum).all()
  ords = [];
  for order in orders:
    user = order.user.to_json()
    cake = order.cake.to_json()
    ords.append(order.to_json(user, cake))
  return jsonify({'orders' : ords})

@api.route('/users/<int:userId>/orders/statusNum')
def get_user_orders_statusNum(userId):
  statusNum = {}
  statuses = db.session.query(Order.status, func.count(Order.status)).filter(Order.userId==userId).group_by(Order.status).all()
  for status in statuses:
    statusNum[status[0]] = status[1]
  return jsonify(statusNum)

@api.route('/orders/cakeNum')
def get_orders_cakeNum():
  cakeNum = {}
  cakes = db.session.query(Order.cakeId, func.count(Order.cakeId)).group_by(Order.cakeId).all()
  for cake in cakes:
    cakeNum[cake[0]] = cake[1]
  return jsonify(cakeNum)

@api.route('/orders/<int:id>')
def get_order(id):
  order = Order.query.get_or_404(id)
  return jsonify(order.to_json(order.user.to_json(), order.cake.to_json()))

@api.route('/users/<int:id>/orders')
def get_user_orders(id):
  user = User.query.get_or_404(id)
  orders = user.orders.all()
  ords = [];
  for order in orders:
    user = order.user.to_json()
    cake = order.cake.to_json()
    ords.append(order.to_json(user, cake))
  return jsonify({'orders' : ords})

@api.route('/users/<int:id>/status/<int:status>/orders')
def get_user_status_orders(id, status):
  user = User.query.get_or_404(id)
  orders = user.orders.filter_by(status=status).all()
  ords = [];
  for order in orders:
    user = order.user.to_json()
    cake = order.cake.to_json()
    ords.append(order.to_json(user, cake))
  return jsonify({'orders' : ords})

@api.route('/orders', methods=['POST'])
def new_order():
  order = Order.from_json(request.json)
  cake = Cake.query.get_or_404(request.json.get('cakeId'))
  user = User.query.get_or_404(request.json.get('userId'))
  order.cake = cake
  order.user = user
  db.session.add(order)
  db.session.commit()
  return jsonify(order.to_json(order.user.to_json(), order.cake.to_json()), 201, {'Location' : url_for('api.get_order', id=order.id, _external=True)})

@api.route('/orders/<int:id>', methods=['PUT'])
def edit_order(id):
  ord = Order.query.get_or_404(id)
  ord.status = request.json.get('status', ord.status)
  print ord.status
  ord.uTimestamp = datetime.now()
  db.session.commit()
  return jsonify(ord.to_json(ord.user.to_json(), ord.cake.to_json()))

