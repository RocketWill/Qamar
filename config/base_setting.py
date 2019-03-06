# -*- coding: UTF-8 -*-
SERVER_PORT = 8999
DEBUG = False
SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME = 'qamar_user'

'''
過濾Url
'''

IGNORE_URLS = [
    "^/user/login",
    "^/api",
    "^/mail"
]

IGNORES_CHECK_LOGIN_URLS = [
    '^/static',
    '^/favicon.ico'
]

SUPER_ADMIN = 'qamar'


PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1":"normal",
    "0":"deleted"
}


MINA_APP = {
    'AppID' : 'wxa8abb1ea36933968',
    'AppSecret':"adfaf55dbb823980e196e7f8db96ef7c"
}

EMAIL_POSTFIX = '@pku.edu.cn'


UPLOAD = {
    'ext':['jpg','gif','bmp','jpeg','png'],
    'prefix_path':"/web/static/upload/",
    'prefix_url':'/static/upload/'
}

APP = {
    'domain':'http://127.0.0.1:8999'
}