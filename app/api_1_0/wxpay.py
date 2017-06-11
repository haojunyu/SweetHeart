#!/usr/bin/env python
# coding=utf-8
from flask import g, jsonify, request, current_app, url_for
from . import api
from .. import db
from ..models import User
from datetime import datetime
import requests, json
from xml.etree import cElementTree as ET

@api.route('/prepay', methods=['GET'])
def get_prepay():
  # 设置统一下单参数
  data = {}
  data['appid'] = current_app.config['APP_ID']
  data['mch_id'] = current_app.config['MCH_ID']
  data['device_info'] = 'WEB'
  data['nonce_str'] = rand_str()
  data['body'] = request.args.get('body')
  if request.args.get('detail'):
    data['detail'] = request.args.get('detail')
    print data['detail']
  data['out_trade_no'] = datetime.now().strftime('%Y%m%d%H%M%s') + rand_str(4)
  data['total_fee'] = str(int(float(request.args.get('total_fee')) * 100))
  data['spbill_create_ip'] = '123.206.190.111'
  data['notify_url'] = request.args.get('notify_url')
  data['trade_type'] = 'JSAPI'
  data['openid'] = g.current_user.openId
  data['sign'] = sign_md5(data)
  xml = ET.Element('xml')
  for key in data:
    ET.SubElement(xml, key).text = data[key]
  print ET.tostring(xml)
  res = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=ET.tostring(xml))

  prepay = {}
  resXml = ET.fromstring(res.content)
  for ele in resXml:
    prepay[ele.tag] = ele.text
  print 'weixin merchant: %s' % prepay
  return jsonify({'prepay' : prepay})

@api.route('/notify', methods=['GET', 'POST'])
def deal_notify():
  # 处理支付结果通知
  print 'data: %s' % request.data
  print 'form: %s' % request.form
  print 'args: %s' % request.args
  print 'get_data: %s' % request.get_data()
  # 返回XML结果
  xml = ET.Element('xml')
  ET.SubElement(xml, 'return_code').text = 'SUCCESS'
  ET.SubElement(xml, 'return_msg').text = 'ok'
  return ET.tostring(xml)



# 生成length长度的随机字符串
def rand_str(len=32):
  import string, random
  return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(len))

# 对dict数据进行MD签名
def sign_md5(data):
  import hashlib
  sign = None
  orderData = []
  if type(data) == dict and data != None:
    for key in sorted(data.keys()):
      orderData.append(key + '=' + data[key])
      print key + '=' + data[key] 
    orderData.append('key=' + current_app.config['API_KEY']) 
    md5Data = '&'.join(orderData)
    sign = hashlib.md5(md5Data).hexdigest().upper()
    return sign
    #return md5Data
  return sign

