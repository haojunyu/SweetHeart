import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'Sweet Heart'
  
  @staticmethod
  def init_app(app):
    pass

# 三个环境可以设置不同的数据库
class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'mysql://hjy@hjy:123.206.190.111/SweetHeart'

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'mysql://hjy@hjy:123.206.190.111/SweetHeart'

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'mysql://hjy@hjy:123.206.190.111/SweetHeart'

# 通过config[name]来选择不同的配置环境
config = {
  'development' : DevelopmentConfig,
  'testing' : TestingConfig,
  'production' : ProductionConfig,
  'default' : DevelopmentConfig
}
