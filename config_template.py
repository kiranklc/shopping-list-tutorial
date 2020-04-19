# This a template for config.py that contains sensitive values

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# DO NOT POST ACTUAL VALUES ON GITHUB


class Auth:
    CLIENT_ID = 'Google client id'
    CLIENT_SECRET = 'Google client secret'
    DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    REDIRECT_URI = 'https://shoppinglist2020.herokuapp.com/login/callback'
    #REDIRECT_URI = 'https://127.0.0.1:5000/login/callback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/oauth2/v2/userinfo'
    SCOPE = ['email','profile','openid']


class Config:
    APP_NAME = "Shopping List"
    SECRET_KEY = 'Secret key for the app'


class DevConfig(Config):
    DEBUG = True
    DATABASE_URI = os.environ.get('DATABASE_URL')  # Add database url as environment variable


class ProdConfig(Config):
    DEBUG = True
    DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}