#!/usr/bin/env python
# coding=utf-8
from flask import jsonify, request, url_for, current_app, jsonify
from . import api
from .authentication import auth
import os

# 检验上传文件类型
def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@api.route('/upload', methods=['POST'])
def upload_file():
  print 'function upload_file'
  if request.method == 'POST':
    file = request.files['file']
    if file and allowed_file(request.form['fileName']):
      filename = request.form['fileName']
      file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
      return jsonify({'status':'success', 'filename':filename})
    return jsonify({'status':'fail', 'reason':'file type is not allowed'})
  return jsonify({'status':'fail', 'reason':'unknow'})
