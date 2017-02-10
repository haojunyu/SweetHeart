#!/usr/bin/env python
# coding=utf-8

from . import db
from flask import url_for
#from app.exceptions import ValidationError

####### class User --> table users
class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True, nullable=False)

  def __init__(self,name):
    self.name = name

  def __repr__(self):
    return 'User %r' % self.name

  # 序列化转换: 资源->JSON
  def to_json(self):
    json_user = {
      'url'   : url_for('api.get_user', id=self.id, _external=True),
      'name'  : self.name
    }
    return json_user

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_user):
    name = json_user.get('name')
#    if body is None or body = '':
#      raise ValidationError('user does not hava a name')
    return User(name=name)


####### class Category --> table categories
class Category(db.Model):
  __tablename__ = 'categories'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), unique=True, nullable=False)
  desc = db.Column(db.String(100))

  def __init__(self, name, desc):
    self.name = name
    self.desc = desc

  def __repr__(self):
    return 'Category %r' % self.name

  # 序列化转换: 资源->JSON
  def to_json(self):
    json_category = {
      'url'   : url_for('api.get_category', id=self.id, _external=True),
      'name'  : self.name,
      'desc'  : self.desc
    }
    return json_category

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_category):
    name = json_category.get('name')
    desc = json_category.get('desc')
#    if body is None or body = '':`
#      raise ValidationError('user does not hava a name')
    return Category(name=name, desc=desc)




