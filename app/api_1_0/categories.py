from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Category 

@api.route('/categories')
def get_categories():
  categories = Category.query.all()
  return jsonify({'categories' : [category.to_json() for category in categories]})

@api.route('/categories/<int:id>')
def get_category(id):
  category = Category.query.get_or_404(id)
  return jsonify(category.to_json())

@api.route('/categories', methods=['POST'])
def new_category():
  category = Category.from_json(request.json)
  db.session.add(category)
  db.session.commit()
  return jsonify(category.to_json(), 201, {'Location' : url_for('api.get_category', id=category.id, _external=True)})

@api.route('/categories', methods=['PUT'])
def edit_category(id):
  category = Category.query.get_or_404(id)
  category.name = request.json.get('name', category.name)
  category.desc = request.json.get('desc', category.desc)
  db.session.add(category)
  return jsonify(category.to_json())

