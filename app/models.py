#!/usr/bin/env python
# coding=utf-8
from . import db, login_manager
from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from datetime import datetime
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
  comments = db.relationship('Comment', backref='user', lazy='dynamic')
  orders = db.relationship('Order', backref='user', lazy='dynamic')

  def __repr__(self):
    return 'User %r' % self.nickName

  # 序列化转换: 资源->JSON
  def to_json(self):
    json_user = {
      'uri'   : url_for('api.get_user', id=self.id, _external=True),
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

  # 生成初始数据
  @staticmethod
  def generate_users():
    user = User(id=1, openId='oAk3s0Bef6kcKKf0waVJvDUlrShE', nickName=u'飘移', gender=1, city='Jinan', province='Shandong', country='CN', avatarUrl='http://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL04eZJ57hiaQcuWk4kT5vvY6Epmmo6smJ94ejJqWZrbTIriaftjBhvDfeIwsxBTM5hibpXx3CiaC9T0Q/0')
    db.session.add(user)
    try:
      db.session.commit()
      print 'generate users successfully'
    except IntegrityError:
      db.session.rollback()
      print 'fail to generate users'


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

  def __repr__(self):
    return 'Category %r' % self.name

  # 序列化转换: 资源->JSON
  def to_json(self):
    json_category = {
      'uri'   : url_for('api.get_category', id=self.id, _external=True),
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

  # 生成初始数据
  @staticmethod
  def generate_categories():
    cateNames = ['cake', 'biscuit', 'pudding', 'chocolate']
    cateDescs = [u'蛋糕', u'饼干', u'布丁', u'巧克力']
    for i in range(len(cateNames)):
      cate = Category(id=i+1, name=cateNames[i], desc=cateDescs[i])
      db.session.add(cate)
    try:
      db.session.commit()
      print 'generate categories successfully'
    except IntegrityError:
      db.session.rollback()
      print 'fail to generate categories'

####### class Cake --> table cakes
class Cake(db.Model):
  __tablename__ = 'cakes'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), unique=True, nullable=False)
  desc = db.Column(db.String(100), nullable=False)
  detail = db.Column(db.String(200))
  price = db.Column(db.Numeric(8,2), nullable=False)
  imgUrl = db.Column(db.String(100),nullable=False)
  stars = db.Column(db.Numeric(2,1), default=3.0)
  cateId = db.Column(db.Integer, db.ForeignKey('categories.id'))
  comments = db.relationship('Comment', backref='cake', lazy='dynamic')
  orders = db.relationship('Order', backref='cake', lazy='dynamic')
  
  def __repr__(self):
    return 'Cake %r' % self.name

  # 序列化转换: 资源->JSON
  def to_json(self, cate=None):
    json_cake = {
      'uri'   : url_for('api.get_cake', id=self.id, _external=True),
      'cakeId'  : self.id,
      'name'  : self.name,
      'desc'  : self.desc,
      'detail': self.detail,
      'price' : str(self.price),
      'imgUrl': self.imgUrl,
      'stars' : str(self.stars),
      'cateId': self.cateId,
      'cate'  : cate
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
    stars = Decimal(json_cake.get('stars'))
    cateId = json_cake.get('cateId')
    return Cake(name=name, desc=desc, detail=detail, price=price, imgUrl=imgUrl, stars=stars, cateId=cateId)

  # 生成初始数据
  @staticmethod
  def generate_cakes():
    cakeNames = ['creamCake', 'fruitCake', 'personalCake', 'mousseCake', 'flowerCake', 'layerCake', 'paperCake']
    cakeDescs = [u'鲜奶蛋糕', u'水果蛋糕', u'个性蛋糕', u'慕斯蛋糕', u'鲜花蛋糕', u'千层蛋糕', u'纸杯蛋糕']
    cakePrices = [58, 58, 118, 78, 78, 128, 32.8]
    for i in range(len(cakeNames)):
      cake = Cake(id=i+11, name=cakeNames[i], desc=cakeDescs[i], detail=u'这是'+cakeDescs[i], price=cakePrices[i], imgUrl=cakeNames[i]+'.jpg', stars=3.0, cateId=1)
      db.session.add(cake)

    cookNames = ['cookies', 'marguerite', 'cartoonCookies', 'cranberryCookies', 'xlkq']
    cookDescs = [u'曲奇饼干', u'玛格丽特', u'卡通饼干', u'蔓越莓饼干', u'昔腊可求']
    cookPrices = [32.8, 32.8, 32.8, 32.8, 32.8]
    for i in range(len(cookNames)):
      cook = Cake(id=i+21, name=cookNames[i], desc=cookDescs[i], detail=u'这是'+cookDescs[i], price=cookPrices[i], imgUrl=cookNames[i]+'.jpg', stars=3.0, cateId=2)
      db.session.add(cook)

    puddNames = ['creamPudding', 'mangoPudding', 'strawberryPudding', 'blueberryPudding']
    puddDescs = [u'奶油布丁', u'芒果布丁', u'草莓布丁', u'蓝莓布丁']
    puddPrices = [32.8, 32.8, 32.8, 32.8]
    for i in range(len(puddNames)):
      pudd = Cake(id=i+31, name=puddNames[i], desc=puddDescs[i], detail=u'这是'+puddDescs[i], price=puddPrices[i], imgUrl=puddNames[i]+'.jpg', stars=3.0, cateId=3)
      db.session.add(pudd)

    chocNames = ['strawberryChocolate', 'lemonChocolate', 'matchaChocolate', 'whiteMilkChocolate', 'bitterSweetChocolate']
    chocDescs = [u'草莓味巧克力', u'柠檬味巧克力', u'抹茶味巧克力', u'白牛奶味巧克力', u'苦甜味巧克力']
    chocPrices = [32.8, 32.8, 32.8, 32.8, 32.8]
    for i in range(len(chocNames)):
      choc = Cake(id=i+41, name=chocNames[i], desc=chocDescs[i], detail=u'这是'+chocDescs[i], price=chocPrices[i], imgUrl=chocNames[i]+'.jpg', stars=3.0, cateId=4)
      db.session.add(choc)

    try:
      db.session.commit()
      print 'generate cakes successfully'
    except IntegrityError:
      db.session.rollback()
      print 'fail to generate cakes'

####### class Comment --> table comments
class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  userId = db.Column(db.Integer, db.ForeignKey('users.id'))
  cakeId = db.Column(db.Integer, db.ForeignKey('cakes.id'))
  stars = db.Column(db.Numeric(2,1), default=3.0)
  comment = db.Column(db.String(200))
  photos = db.relationship('Picture', backref='comment', lazy='dynamic')
  timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

  def __repr__(self):
    return 'Comment: %r' % (self.comment)

  # 序列化转换: 资源->JSON
  def to_json(self, user=None, cake=None, photos=None):
    json_comment = {
      'uri'   : url_for('api.get_comment', id=self.id, _external=True),
      'userUri': url_for('api.get_user', id=self.userId, _external=True),
      'user'  : user,
      'cakeUri': url_for('api.get_cake', id=self.cakeId, _external=True),
      'cake'  : cake,
      'stars' : str(self.stars),
      'comment' : self.comment,
      'photos': photos,
      'timestamp': self.timestamp.strftime('%Y-%m-%d')
    }
    return json_comment

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_comment):
    userId = json_comment.get('userId')
    cakeId = json_comment.get('cakeId')
    stars = Decimal(json_comment.get('stars'))
    comment = json_comment.get('comment')
    return Comment(userId=userId, cakeId=cakeId, stars=stars, comment=comment)

  # 生成初始数据
  @staticmethod
  def generate_comments():
    cakeIds = [11, 21, 31, 41]
    stars = [2, 3, 4, 5]
    comments = [u'我爱蛋糕', u'喜欢饼干', u'爱吃布丁', u'最爱巧克力']
    for i in range(len(cakeIds)):
      comm = Comment(id=i+1, userId=1, cakeId=cakeIds[i], stars=stars[i], comment=comments[i])
      db.session.add(comm)
    try:
      db.session.commit()
      print 'generate comments successfully'
    except IntegrityError:
      db.session.rollback()
      print 'fail to generate comments'


####### class Picture --> table pictures
class Picture(db.Model):
  __tablename__ = 'pictures'
  id = db.Column(db.Integer, primary_key=True)
  commentId = db.Column(db.Integer, db.ForeignKey('comments.id'))
  picName = db.Column(db.String(100))

  def __repr__(self):
    return 'Picture: %r' % (self.picName)

  # 序列化转换: 资源->JSON
  def to_json(self):
    json_picture = {
      'uri'   : url_for('api.get_picture', id=self.id, _external=True),
      'commentId' : self.commentId,
      'picName': self.picName
    }
    return json_picture

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_picture):
    commentId = json_picture.get('commentId')
    picName = json_picture.get('picName')
    return Picture(commentId=commentId, picName=picName)

  # 生成初始数据
  @staticmethod
  def generate_pictures():
    commentIds = [1, 3, 3]
    pics = ['1_creamCake.jpg', '1_creamPudding.jpg', '1_strawberryPudding.jpg']
    for i in range(len(commentIds)):
      pic = Picture(id=i+1, commentId=commentIds[i], picName=pics[i])
      db.session.add(pic)
    try:
      db.session.commit()
      print 'generate pictures successfully'
    except IntegrityError:
      db.session.rollback()
      print 'fail to generate pictures'


####### class Order --> table orders
class Order(db.Model):
  __tablename__ = 'orders'
  id = db.Column(db.Integer, primary_key=True)
  userId = db.Column(db.Integer, db.ForeignKey('users.id'))
  cakeId = db.Column(db.Integer, db.ForeignKey('cakes.id'))
  status = db.Column(db.Integer, default=0) # 1-order, 2-consume, 3-comment
  prepayId = db.Column(db.String(64), unique=True, nullable=False)
  cTimestamp = db.Column(db.DateTime, index=True, default=datetime.now())
  uTimestamp = db.Column(db.DateTime, default=datetime.now())

  def __repr__(self):
    return 'Order: %r' % (self.prepayId)

  # 序列化转换: 资源->JSON
  def to_json(self, user=None, cake=None):
    json_order = {
      'uri'   : url_for('api.get_order', id=self.id, _external=True),
      'orderId': self.id,
      'userUri': url_for('api.get_user', id=self.userId, _external=True),
      'user'  : user,
      'cakeUri': url_for('api.get_cake', id=self.cakeId, _external=True),
      'cake'  : cake,
      'status' : self.status,
      'prepayId' : self.prepayId,
      'cTimestamp': self.cTimestamp.strftime('%Y-%m-%d'),
      'uTimestamp': self.uTimestamp
    }
    return json_order

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_order):
    userId = json_order.get('userId')
    cakeId = json_order.get('cakeId')
    status = json_order.get('status')
    prepayId = json_order.get('prepayId')
    return Order(userId=userId, cakeId=cakeId, status=status, prepayId=prepayId)

  # 生成初始数据
  @staticmethod
  def generate_orders():
    cakeIds = [11, 21, 31, 41]
    statuses = [1, 2, 3, 3]
    prepayIds = ['wx1', 'wx2', 'wx3', 'wx4']
    for i in range(len(cakeIds)):
      order = Order(id=i+1, userId=1, cakeId=cakeIds[i], status=statuses[i], prepayId=prepayIds[i])
      db.session.add(order)
    try:
      db.session.commit()
      print 'generate orders successfully'
    except IntegrityError:
      db.session.rollback()
      print 'fail to generate orders'


