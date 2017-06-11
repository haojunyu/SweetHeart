#!/usr/bin/env python
# coding=utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or '5bf030dbb13422031ea802a9ab75900a'
  API_KEY = os.environ.get('API_KEY') or '666ZhangWangLuTin00SweetHeart999'
  APP_ID = 'wx1bd3022be6b18895'
  MCH_ID = '1443221402'
  UPLOAD_FOLDER = '/home/ubuntu/SweetHeart/imgs/upload'
  ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'JPG',  'jpeg', 'gif'])
  
  @staticmethod
  def init_app(app):
    pass

# 三个环境可以设置不同的数据库
class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'mysql://hjy:hjy@localhost/SweetHeart?charset=utf8'

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'mysql://hjy:hjy@localhost/SHTest?charset=utf8'

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'mysql://hjy:hjy@localhost/SweetHeart?charset=utf8'

# 通过config[name]来选择不同的配置环境
config = {
  'development' : DevelopmentConfig,
  'testing' : TestingConfig,
  'production' : ProductionConfig,
  'default' : DevelopmentConfig
}
