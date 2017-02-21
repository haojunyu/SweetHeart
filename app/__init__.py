#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

# 数据库
db = SQLAlchemy()

# 登录模块
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  # 将扩展对象绑定到应用上
  db.init_app(app)
  login_manager.init_app(app)

  # 注册授权服务蓝本
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix='/auth')

  # 注册主程序蓝本，解决路由和自定义错误页面处理程序
  #from .main import main as main_blueprint
  #app.register_blueprint(main_blueprint)

  # 注册REST Web服务蓝本
  from .api_1_0 import api as api_1_0_blueprint
  app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

  return app
