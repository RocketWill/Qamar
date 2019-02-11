# -*- coding: UTF-8 -*-
SERVER_PORT = 8999
DEBUG = False
SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME = 'qamar_user'

'''
過濾Url
'''

IGNORE_URLS = [
    "^/user/login"
]

IGNORES_CHECK_LOGIN_URLS = [
    '^/static',
    '^/favicon.ico'
]