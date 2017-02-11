from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Category, Cake 

@api.route('/cakes')
def get_cakes():
  cakes = Cake.query.all()
  return jsonify({'cakes' : [cake.to_json() for cake in cakes]})

@api.route('/cakes/<int:id>')
def get_cake(id):
  cake = Cake.query.get_or_404(id)
  return jsonify(cake.to_json())

@api.route('/categories/<int:id>/cakes')
def get_categories_cakes(id):
  category = Category.query.get_or_404(id)
  cakes = category.cakes.all()
  return jsonify({'cakes' : [cake.to_json() for cake in cakes]})

@api.route('/categories/<int:id>/cakes', methods=['POST'])
def new_cake(id):
  category = Category.query.get_or_404(id)
  cake = Cake.from_json(request.json)
  cake.category = category
  db.session.add(cake)
  db.session.commit()
  return jsonify(cake.to_json(), 201, {'Location' : url_for('api.get_cake', id=cake.id, _external=True)})

@api.route('/cakes/<int:id>', methods=['PUT'])
def edit_cake(id):
  cake = Cake.query.get_or_404(id)
  cake.name = request.json.get('name', cake.name)
  cake.desc = request.json.get('desc', cake.desc)
  cake.detail = request.json.get('detail', cake.detail)
  cake.price = request.json.get('price', cake.price)
  cake.imgUrl = request.json.get('imgUrl', cake.imgUrl)
  db.session.add(cake)
  return jsonify(cake.to_json())

