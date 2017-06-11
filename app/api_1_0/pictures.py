from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Picture
from .authentication import auth

@api.route('/pictures')
#@auth.login_required
def get_pictures():
  pictures = Picture.query.all()
  return jsonify({'pictures' : [picture.to_json() for picture in pictures]})

@api.route('/pictures/<int:id>')
def get_picture(id):
  picture = Picture.query.get_or_404(id)
  return jsonify(picture.to_json())

@api.route('/pictures', methods=['POST'])
def new_picture():
  picture = Picture.from_json(request.json)
  db.session.add(picture)
  db.session.commit()
  return jsonify(picture.to_json(), 201, {'Location' : url_for('api.get_picture', id=picture.id, _external=True)})

@api.route('/pictures', methods=['PUT'])
def edit_picture(id):
  picture = Picture.query.get_or_404(id)
  picture.picName = request.json.get('picName', picture.picName)
  db.session.add(picture)
  return jsonify(picture.to_json())

