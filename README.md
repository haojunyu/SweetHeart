# SweetHeart
基于flask的web应用，为微信小程序SweetHeart提供后台服务

框架
flask
restful api


## 目录框架
* app/ 用于存放应用
  * templates/
  * statics/
  * main/ 主程序
    * __init__.py 创建蓝本
    * errors.py 错误处理
    * forms.py
    * views.py  程序的路由
  * api_1_0/  REST Web服务
    * __init__.py 创建蓝本
    * modelName.py  具体模块
    * errors.py 错误处理
  * __init__.py
  * email.py
  * models.py
* migrations/ 数据库迁移脚本
* tests/  单元测试
  * __init__.py
  * test*.py
* venv/ 这里是开发所需要的python虚拟环境，用virtualenvwrapper管理后，该文件在$HOME/.virtualenv/下面
* requirements.txt 项目所有依赖包 `pip freeze > requirements.txt`
* config.py 配置文件
* manage.py 用于启动程序
