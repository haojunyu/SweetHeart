#!/usr/bin/env python
# coding=utf-8
from flask import jsonify
from app.exceptions import ValidationError
from . import api

# 无效请求
def bad_request(message):
  response = jsonify({'error': 'bad request', 'message': message})
  response.status_code = 400
  return response


# 未授权请求
def unauthorized(message):
  response = jsonify({'error': 'unauthorized', 'message': message})
  response.status_code = 401
  return response


# 禁止访问
def forbidden(message):
  response = jsonify({'error': 'forbidden', 'message': message})
  response.status_code = 403
  return response


@api.errorhandler(ValidationError)
def validation_error(e):
  return bad_request(e.args[0])
