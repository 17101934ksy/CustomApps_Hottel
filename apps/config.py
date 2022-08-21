import os

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_007')


    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static')    
    
class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'   , 'mysql'),
        os.getenv('DB_USERNAME' , 'root'),
        os.getenv('DB_PASS'     , '1234'),
        os.getenv('DB_HOST'     , 'localhost'),
        os.getenv('DB_PORT'     , 3306),
        os.getenv('DB_NAME'     , 'test')
    ) 

class DebugConfig(Config):
    DEBUG = True

config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}