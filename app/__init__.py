#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  # 将扩展对象绑定到应用上
  db.init_app(app)


  # 注册主程序蓝本，解决路由和自定义错误页面处理程序
  #from .main import main as main_blueprint
  #app.register_blueprint(main_blueprint)

  # 注册REST Web服务蓝本
  from .api_1_0 import api as api_1_0_blueprint
  app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

  return app
