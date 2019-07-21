# /src/config.py

import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    """
    Development environment configuration
    """
    DEBUG = True
    DEVELOPMENT = True


class Production(Config):
    """
    Production enviroConfignment configurations
    """
    DEBUG = False


class Testing(Config):
    """
    Development environment configuration
    """
    TESTING = True


class Staging(Config):
    """
    Staging environment configuration
    """
    DEVELOPMENT = True
    DEBUG = True


app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing,
    'staging': Staging
}
