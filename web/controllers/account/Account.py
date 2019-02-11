# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, g, request, redirect
from common.libs.Helper import ops_render, iPagination
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.models.User import User

from application import app, db

route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    resp_data = {}
    query = User.query
    req = request.values
    page = int(req['page']) if ('page' in req and req['page']) else 1

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': '/account/index'
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(User.uid.desc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['current'] = 'user'
    return ops_render('account/index.html', resp_data)


@route_account.route('/info')
def info():
    resp_data = {}
    req = request.args
    uid = int(req.get('id',0))
    if uid < 1:
        return redirect(UrlManager.buildUrl('/account/index'))

    info = User.query.filter_by(uid = uid).first()
    if not info:
        return redirect(UrlManager.buildUrl('/account/index'))

    resp_data['info'] = info
    resp_data['current'] = 'user'
    return ops_render('account/info.html', resp_data)


@route_account.route('/reset-pwd')
def set():
    res = {'current': 'user'}
    return ops_render('account/index.html', res)
