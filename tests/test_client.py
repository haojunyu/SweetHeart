#!/usr/bin/env python
# coding=utf-8
import unittest
from app import create_app, db
from flask import url_for


class FlaskClientTestCase(unittest.TestCase):
  # 初始化工作
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()
    self.client = self.app.test_client(use_cookies=True)

  # 退出清理工作
  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
  
  # 测试授权主页 
  def test_secret_page(self):
    response = self.client.get(url_for('auth.secret'))
    self.assertTrue('authenticated users' in response.get_data(as_text=True))
