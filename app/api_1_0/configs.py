from flask import jsonify, request, url_for
from . import api
from .. import db
from ..models import Config
from .authentication import auth


@api.route('/initConfigs')
def init_configs():
  configs = Config.query.all()
  configs_dict = {}
  for config in configs:
    configs_dict[config.key] = config.value
  return jsonify({'configs' : configs_dict})

@api.route('/configs')
def get_configs():
  configs = Config.query.all()
  return jsonify({'configs' : [config.to_json() for config in configs]})

@api.route('/configs/<int:id>')
def get_config(id):
  config = Config.query.get_or_404(id)
  return jsonify(config.to_json())

@api.route('/configs', methods=['POST'])
def new_config():
  config = Config.from_json(request.json)
  db.session.add(config)
  db.session.commit()
  return jsonify(config.to_json(), 201, {'Location' : url_for('api.get_config', id=config.id, _external=True)})

@api.route('/configs/<int:id>', methods=['PUT'])
def edit_config(id):
  config = Config.query.get_or_404(id)
  config.value = request.json.get('value', config.value)
  db.session.add(config)
  return jsonify(config.to_json())

