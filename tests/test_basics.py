#!/usr/bin/env python
# coding=utf-8
import unittest
from flask import current_app
from app import create_app,db

class BasicTestCase(unittest.TestCase):
  # 初始化工作
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  # 退出清理工作
  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  # 测试app是否存在
  def test_app_exists(self):
    self.assertFalse(current_app is None)

  # 测试app是否是testing
  def test_app_is_testing(self):
    self.assertTrue(current_app.config['TESTING'])
