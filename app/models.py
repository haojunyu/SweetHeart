#!/usr/bin/env python
# coding=utf-8
from . import db, login_manager
from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin
from decimal import Decimal
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from app.exceptions import ValidationError

####### class User --> table users
class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  openId = db.Column(db.String(50), unique=True, nullable=False)
  nickName = db.Column(db.String(100), nullable=False)
  gender = db.Column(db.Integer)
  city = db.Column(db.String(40))
  province = db.Column(db.String(40))
  country = db.Column(db.String(40))
  avatarUrl = db.Column(db.String(200))

#  def __init__(self,name):
#    self.name = name

  def __repr__(self):
    return 'User %r' % self.openId

  # 序列化转换: 资源->JSON
  def to_json(self):
    json_user = {
      'url'   : url_for('api.get_user', id=self.id, _external=True),
      'openId'  : self.openId,
      'nickName'  : self.nickName,
      'gender'  : self.gender,
      'city'  : self.city,
      'province'  : self.province,
      'country'  : self.country,
      'avatarUrl'  : self.avatarUrl
    }
    return json_user

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_user):
    openId = json_user.get('openId')
    nickName = json_user.get('nickName')
    gender = json_user.get('gender')
    city = json_user.get('city')
    province = json_user.get('province')
    country = json_user.get('country')
    avatarUrl = json_user.get('avatarUrl')
#    if body is None or body = '':
#      raise ValidationError('user does not hava a name')
    return User(openId=openId, nickName=nickName, gender=gender, city=city, province=province, country=country, avatarUrl=avatarUrl)

  # 生成授权token
  def generate_auth_token(self, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'openId': self.openId})

  # 验证授权token
  @staticmethod
  def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      data = s.loads(token)
      print data
    except:
      return None
    return User.query.filter_by(openId=data['openId']).first()


# user_loader回调，用于从会话中存储的用户ID重新加载用户对象
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


####### class AnonymousUser --> no table 
class AnonymousUser(AnonymousUserMixin):
  def can(self, permissions):
    return False

  def is_administrator(self):
    return False
login_manager.anonymous_user = AnonymousUser


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

  def __init__(self, name, desc, detail, price, imgUrl, orders, stars, cateId):
    self.name = name
    self.desc = desc
    self.detail = detail
    self.price = price
    self.imgUrl = imgUrl
    self.orders = orders
    self.stars = stars
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
      'price' : str(self.price),
      'imgUrl': self.imgUrl,
      'orders': self.orders,
      'stars' : self.stars,
      'cateId': self.cateId
    }
    return json_cake

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_cake):
    name = json_cake.get('name')
    desc = json_cake.get('desc')
    detail = json_cake.get('detail')
    price = Decimal(json_cake.get('price'))
    imgUrl = json_cake.get('imgUrl')
    orders = json_cake.get('orders')
    stars = json_cake.get('stars')
    cateId = json_cake.get('cateId')
    return Cake(name=name, desc=desc, detail=detail, price=price, imgUrl=imgUrl, orders=orders, stars=stars, cateId=cateId)





