# -*- coding: UTF-8 -*-
import os
DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/qamar_db'
SQLALCHEMY_TRACK_MODIFICATION = False
SQLALCHEMY_ENCODING = 'utf-8'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ['email_account']
MAIL_PASSWORD = os.environ['email_pwd']
MAIL_DEFAULT_SENDER = 'Qamar'+' '+os.environ['email_account']