from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import User, Cake, Comment 

@api.route('/comments')
def get_comments():
  comments = Comment.query.all()
  comms = [];
  for comment in comments:
    user = comment.user.to_json()
    cake = comment.cake.to_json()
    pics = [pic.to_json() for pic in comment.photos.all()]
    comms.append(comment.to_json(user, cake, pics))
  return jsonify({'comments' : comms})

@api.route('/comments/<int:id>')
def get_comment(id):
  comment = Comment.query.get_or_404(id)
  pics = [pic.to_json() for pic in comment.photos.all()]
  return jsonify(comment.to_json(comment.user.to_json(), comment.cake.to_json(), pics))

@api.route('/users/<int:id>/comments')
def get_user_comments(id):
  user = User.query.get_or_404(id)
  comments = user.comments.all()
  comms = [];
  for comment in comments:
    user = comment.user.to_json()
    cake = comment.cake.to_json()
    pics = [pic.to_json() for pic in comment.photos.all()]
    comms.append(comment.to_json(user, cake, pics))
  return jsonify({'comments' : comms})

@api.route('/cakes/<int:id>/comments')
def get_cake_comments(id):
  cake = Cake.query.get_or_404(id)
  comments = cake.comments.all()
  comms = [];
  for comment in comments:
    user = comment.user.to_json()
    cake = comment.cake.to_json()
    pics = [pic.to_json() for pic in comment.photos.all()]
    comms.append(comment.to_json(user, cake, pics))
  return jsonify({'comments' : comms})

@api.route('/comments', methods=['POST'])
def new_comment():
  print request.json
  comment = Comment.from_json(request.json)
  cake = Cake.query.get_or_404(request.json.get('cakeId'))
  user = User.query.get_or_404(request.json.get('userId'))
  comment.cake = cake
  comment.user = user
  db.session.add(comment)
  db.session.commit()
  return jsonify(comment.to_json(comment.user.to_json(), comment.cake.to_json(), None), 201, {'Location' : url_for('api.get_comment', id=comment.id, _external=True), 'commentId':comment.id})

@api.route('/comments/<int:id>', methods=['PUT'])
def edit_comment(id):
  comm = Comment.query.get_or_404(id)
  comm.stars = request.json.get('stars', comm.stars)
  comm.comment = request.json.get('comment', comm.comment)
  comm.timestamp = request.json.get('timestamp', comm.timestamp)
  db.session.add(comm)
  pics = [pic.to_json() for pic in comm.photos]
  return jsonify(comm.to_json(comm.user.to_json(), comm.cake.to_json(), pics))

