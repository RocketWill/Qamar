# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, g, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.models.log.AppAccessLog import AppAccessLog
from common.libs.UrlManager import UrlManager
from common.models.member.Member import Member
from sqlalchemy import or_

from application import app, db

route_member = Blueprint('member_page', __name__)

@route_member.route('/index')
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Member.query


    if 'mix_kw' in req:
        rule = or_(Member.nickname.ilike("%{0}%".format(req['mix_kw'])), Member.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Member.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page),"")
    }

    pages = iPagination(page_params)
    offset = (page -1) * app.config['PAGE_SIZE']
    list = query.order_by(Member.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] ='member'

    return ops_render('member/index.html', resp_data)

@route_member.route('/info')
def info():
    resp_data = {}
    req = request.args
    id = int(req.get('id', 0))
    if id < 1:
        return redirect(UrlManager.buildUrl('/member/index'))

    info = Member.query.filter_by(id=id).first()
    if not info:
        return redirect(UrlManager.buildUrl('/member/index'))

    #access_log = AppAccessLog.query.filter_by(uid=uid)
    #access_log = access_log.order_by(AppAccessLog.created_time.desc()).all()[0:20]

    resp_data['info'] = info

    resp_data['info'] = info
    resp_data['current'] = 'member'
    return ops_render('member/info.html', resp_data)

@route_member.route('/set', methods = ["GET", "POST"])
def set():
    resp_data = {}
    resp_data['current'] = 'member'
    if request.method == "GET":
        req = request.args
        id = int(req.get("id",0))
        if id < 1:
            return redirect(UrlManager.buildUrl('/member/index'))

        user_info = Member.query.filter_by(id=id).first()
        if not user_info:
            return redirect(UrlManager.buildUrl('/member/index'))

        if user_info.status != 1:
            return redirect(UrlManager.buildUrl('/member/index'))

        resp_data['user_info'] = user_info
        return ops_render('member/set.html', resp_data)

    resp = {'code':200,'msg':"操作成功","data":{}}
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    id = int(req['id']) if 'id' in req else 0
    email_check = int(req['email_check']) if 'email_check' in req else -1

    if nickname == None or len(nickname) < 3:
        resp['code'] = -1
        resp['msg'] = "請輸入符合規範的使用者名稱"
        return jsonify(resp)

    user_info = Member.query.filter_by(id=id).first()
    if not  user_info:
        resp['code'] = -1
        resp['msg'] = "查無此使用者"
        return jsonify(resp)

    user_info.nickname = nickname

    if email_check > -1:
        user_info.email_validation = email_check

    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)


@route_member.route("/ops", methods=['POST'])
def ops():
    resp = {'code': 200, 'msg': "操作成功", "data": {}}
    req = request.values

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

    member_info = Member.query.filter_by(id=id).first()

    if not member_info:
        resp['code'] = -1
        resp['msg'] = '查無此會員，請重試'
        return jsonify(resp)

    if act == "remove":
        member_info.status = 0
    elif act == "recover":
        member_info.status = 1

    db.session.add(member_info)
    db.session.commit()

    return jsonify(resp)







