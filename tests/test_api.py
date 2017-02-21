#!/usr/bin/env python
# coding=utf-8
import unittest
from app import create_app, db


class APITestCase(unittest.TestCase):
  # 初始化工作
  def setUp(self):
    self.app = create_app()
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  # 退出清理工作
  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
