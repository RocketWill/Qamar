# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, g
from common.libs.Helper import ops_render

route_account = Blueprint('account_page', __name__)

@route_account.route('/index')
def index():
    return ops_render('account/index.html',{'item':g.current_user})

@route_account.route('/info')
def info():
    return ops_render('account/info.html')

@route_account.route('/reset-pwd')
def set():
    return ops_render('account/index.html')