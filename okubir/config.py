import os

class BaseConfig(object):
    SECRET_KEY = "\x85\xb6u\x82\xc4\xdc\x91\xa9\x10a\x87\xe4\xc5\xde&\x89|\xa5(\xa6\xaa\xa1s\xf4"
    
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'test'
    SECURITY_REGISTERABLE = True
    SECURITY_REGISTER_URL = '/register_user'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    UPLOADS_DEFAULT_DEST = os.environ.get('UPLOAD_PATH')

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
