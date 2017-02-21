#!/usr/bin/env python
# coding=utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or '426ccb3829fc784b62ddfb6f3c20e169'
  APPID = 'wx29ac02cb7e383f87'
  
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
