from flask import jsonify
from app.exceptions import ValidationError
from . import auth


def bad_request(message):
  response = jsonify({'error': 'bad request', 'message': message})
  response.status_code = 400
  return response


@auth.errorhandler(ValidationError)
def validation_error(e):
   return bad_request(e.args[0])
