# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, g, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.models.log.AppAccessLog import AppAccessLog
from common.libs.UrlManager import UrlManager
from common.models.User import User
from sqlalchemy import or_

from application import app, db

route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    resp_data = {}
    query = User.query
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    if 'mix_kw' in req:
        rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])), User.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page),"")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(User.uid.desc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['super_admin'] = app.config['SUPER_ADMIN']
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


    access_log = AppAccessLog.query.filter_by(uid = uid)
    access_log = access_log.order_by(AppAccessLog.created_time.desc()).all()[0:20]

    resp_data['info'] = info
    resp_data['access_log'] = access_log
    resp_data['access_log_len'] = len(access_log)


    resp_data['info'] = info
    resp_data['current'] = 'user'
    return ops_render('account/info.html', resp_data)


@route_account.route('/set', methods=["GET", "POST"])
def set():
    default_pwd = "*****"
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int(req.get("id", 0))
        user_info = None
        if uid:
            user_info = User.query.filter_by(uid = uid).first()

        if user_info.nickname == app.config['SUPER_ADMIN']:
            return redirect(UrlManager.buildUrl('/account/index'))

        resp_data['user_info'] = user_info
        resp_data['current'] = 'user'
        return ops_render('account/set.html', resp_data)

    resp = {'code': 200, 'msg': "操作成功", 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0

    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    email = req['email'] if 'email' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "請輸入符合規範的用戶名稱"
        return jsonify(resp)

    if mobile is None or len(mobile) < 11:
        resp['code'] = -1
        resp['msg'] = "請輸入符合規範的手機號"
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "請輸入符合規範的郵箱"
        return jsonify(resp)

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = "請輸入符合規範的登錄名稱"
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 6:
        resp['code'] = -1
        resp['msg'] = "請輸入符合規範的密碼"
        return jsonify(resp)

    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "該登錄名稱已存在，請重新輸入"
        return jsonify(resp)

    user_info = User.query.filter_by(uid = id).first()

    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.login_salt = UserService.geneSalt()
        model_user.created_time = getCurrentDate()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name

    if login_pwd != default_pwd:
        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
    model_user.updated_time = getCurrentDate()


    db.session.add(model_user)
    db.session.commit()

    return jsonify(resp)


@route_account.route('/ops', methods=["POST"])
def ops():
    req = request.values
    resp = {'code': 200, 'msg': "操作成功", 'data': {}}

    id = req['id'] if 'id' in req else ""
    act = req['act'] if 'act' in req else ""

    if not id:
        resp['code'] = -1
        resp['msg'] = "請選擇要操作的帳號"
        return jsonify(resp)

    if act not in ["remove", "recover"]:
        resp['code'] = -1
        resp['msg'] = '操作有誤，請重試'
        return jsonify(resp)

    user_info = User.query.filter_by(uid = id).first()

    if not user_info:
        resp['code'] = -1
        resp['msg'] = '指定帳號不存在'
        return jsonify(resp)

    if user_info.nickname == app.config['SUPER_ADMIN']:
        resp['code'] = -1
        resp['msg'] = '禁止刪除超級管理員'
        return jsonify(resp)

    if act == "remove":
        user_info.status = 0

    if act == "recover":
        user_info.status = 1

    user_info.update_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()

    return jsonify(resp)



