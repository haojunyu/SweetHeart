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
  desc = db.Column(db.String(100), nullable=False)
  cakes = db.relationship('Cake', backref='category', lazy='dynamic')

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


####### class Cake --> table cakes
class Cake(db.Model):
  __tablename__ = 'cakes'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), unique=True, nullable=False)
  desc = db.Column(db.String(100), nullable=False)
  detail = db.Column(db.String(200))
  price = db.Column(db.Numeric(8,2), nullable=False)
  imgUrl = db.Column(db.String(100),nullable=False)
  orders = db.Column(db.Integer, default=0)
  stars = db.Column(db.Integer, default=3)
  cateId = db.Column(db.Integer, db.ForeignKey('categories.id'))

  def __init__(self, name, desc, detail, price, imgUrl, cateId):
    self.name = name
    self.desc = desc
    self.detail = detail
    self.detail = price
    self.imgUrl = imgUrl
    self.cateId = cateId

  def __repr__(self):
    return 'Cake %r' % self.name

  # 序列化转换: 资源->JSON
  def to_json(self):
    json_cake = {
      'url'   : url_for('api.get_cake', id=self.id, _external=True),
      'name'  : self.name,
      'desc'  : self.desc,
      'detail': self.detail,
      'imgUrl': self.imgUrl,
      'cateId': self.cateId
    }
    return json_cake

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_cake):
    name = json_cake.get('name')
    desc = json_cake.get('desc')
    detail = json_cake.get('detail')
    imgUrl = json_cake.get('imgUrl')
    cateId = json_cake.get('cateId')
    return Cake(name=name, desc=desc, detail=detail, imgUrl=imgUrl, cateId=cateId)





