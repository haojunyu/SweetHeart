#!/usr/bin/env python
# coding=utf-8
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from . import api
from .errors import unauthorized, forbidden
from ..models import User, AnonymousUser

auth = HTTPBasicAuth()

# 授权进行的验证
@auth.verify_password
def verify_password(openid_or_token, password):
  print 'api: verify password'
  print openid_or_token
  if openid_or_token == '':
    print 'openid_or_token == null'
    g.current_user = AnonymousUser()
    return True
  user = User.verify_auth_token(openid_or_token)
  if user:
    # token登录
    print 'token'
    g.token_used = True
  else:
    user = User.query.filter_by(openId=openid_or_token).first()
    if user:
      # openId登录
      print 'token'
      g.token_used = False
    else:
      # 非token和openId登录
      return False
  g.current_user = user
  print g.token_used, user
  return True

# 授权失败返回的错误
@auth.error_handler
def auth_error():
  return unauthorized('Invalid credentials')

@api.before_request
@auth.login_required
def before_request():
  print 'api: before request'
  if g.current_user.is_anonymous:
    return forbidden('Anonymous Account')

# 获取token
@api.route('/token')
def get_token():
  if g.current_user.is_anonymous or g.token_used:
    return unauthorized('Invalid credentials')
  return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiratioin': 3600})
