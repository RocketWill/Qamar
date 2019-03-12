# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, g, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.models.log.AppAccessLog import AppAccessLog
from common.libs.UrlManager import UrlManager
from common.models.User import User
from common.models.UserGroup import UserGroup
from common.models.question.Question import Question
from common.models.reply.Reply import Reply
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

    user_group_info = UserGroup.query.filter_by(id=info.group_id).first()


    access_log = AppAccessLog.query.filter_by(uid = uid)
    access_log = access_log.order_by(AppAccessLog.created_time.desc()).all()[0:20]

    resp_data['user_group_info'] = user_group_info
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
        user_group_id = int(req.get("user_group_id", -1))

        # if not uid:
        #     return redirect(UrlManager.buildUrl('/account/index'))

        user_info = User.query.filter_by(uid = uid).first()
        # if not user_info:
        #     return redirect(UrlManager.buildUrl('/account/index'))


        if user_info != None and user_info.nickname == app.config['SUPER_ADMIN']:
            return redirect(UrlManager.buildUrl('/account/index'))

        #驗證用戶組
        if user_group_id < 0:
            return redirect(UrlManager.buildUrl('/account/group-set'))

        user_group_info = UserGroup.query.filter_by(id = user_group_id)
        if not user_group_info:
            return redirect(UrlManager.buildUrl('/account/group-set'))




        resp_data['user_group_info'] = user_group_info.first()
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
    user_group_id = int(req['user_group_id']) if 'user_group_id' in req else -1

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

    #驗證用戶組
    if user_group_id < 1 or not user_group_id:
        resp['code'] = -1
        resp['msg'] = "查詢不到該用戶組"
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
    model_user.group_id = user_group_id

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
    grp_id = req['grp_id'] if 'grp_id' in req else ""
    act = req['act'] if 'act' in req else ""

    if grp_id:
        user_group_info = UserGroup.query.filter_by(id=grp_id).first()
        if not user_group_info:
            resp['code'] = -1
            resp['msg'] = "請選擇要操作的用戶組"
            return jsonify(resp)
        if act not in ["remove", "recover"]:
            resp['code'] = -1
            resp['msg'] = '操作有誤，請重試'
            return jsonify(resp)

        if act == "remove":
            user_group_info.status = 0
            #將用戶標記為無效
            user_list = User.query.filter_by(group_id=grp_id).all()
            if user_list:
                for user in user_list:
                    user.status = 0
                    user.updated_time = getCurrentDate()
                    db.session.add(user)
                    db.session.commit()
            question_list = Question.query.filter_by(group_id=grp_id).all()
            q_id_list = []
            for q in question_list:
                q_id_list.append(q.id)

            reply_list = Reply.query.all()
            if reply_list:
                for reply in reply_list:
                    if reply.qid in q_id_list:
                        reply.status = 0
                        #question.updated_time = getCurrentDate()
                        db.session.add(reply)
                        db.session.commit()



        if act == "recover":
            user_group_info.status = 1
            # 將用戶標記為有效
            user_list = User.query.filter_by(group_id=grp_id).all()
            if user_list:
                for user in user_list:
                    user.status = 1
                    user.updated_time = getCurrentDate()
                    db.session.add(user)
                    db.session.commit()
            question_list = Question.query.filter_by(group_id=grp_id).all()
            q_id_list = []
            for q in question_list:
                q_id_list.append(q.id)

            # reply_list = Reply.query.all()
            # if reply_list:
            #     for reply in reply_list:
            #         if reply.qid in q_id_list:
            #             reply.status = 1
            #             # question.updated_time = getCurrentDate()
            #             db.session.add(reply)
            #             db.session.commit()

        user_group_info.update_time = getCurrentDate()
        db.session.add(user_group_info)
        db.session.commit()

        return jsonify(resp)

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

@route_account.route('/group-set', methods=["GET", "POST"])
def groupSet():
    resp_data={}
    req = request.values
    status = int(req['status']) if 'status' in req else -1

    query = UserGroup.query
    if status > -1:
        query = query.filter(UserGroup.status==status)

    group_list = query.order_by(UserGroup.weight.desc())

    resp_data['group_list'] = group_list
    resp_data['current'] = 'account'
    resp_data['current_user'] = g.current_user
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render('account/group-set.html', resp_data)

@route_account.route('/group-edit',methods=['GET', 'POST'])
def groupEdit():
    if request.method == "GET":
        resp_data = {}
        user_info = g.current_user
        resp_data['current'] = 'account'
        resp_data['current_user'] = g.current_user
        return ops_render('account/group-edit.html', resp_data)

    resp = {'code': 200, 'msg': "操作成功", 'data': {}}
    req = request.values
    group_name = req['name'] if 'name' in req else ''
    group_des = req['description'] if 'description' in req else ''
    group_weight = int(req['weight']) if 'weight' in req else 1

    if not group_name or len(group_name) < 2:
        resp['code'] = -1
        resp['msg'] = '請輸入符合規範的組名'
        return jsonify(resp)

    if not group_weight or int(group_weight) < 1:
        resp['code'] = -1
        resp['msg'] = '請輸入符合規範的權重'
        return jsonify(resp)

    user_grp = UserGroup()
    user_grp.name = group_name
    user_grp.summary = group_des
    user_grp.weight = group_weight
    user_grp.updated_time = user_grp.created_time = getCurrentDate()
    db.session.add(user_grp)
    db.session.commit()
    return jsonify(resp)

@route_account.route('/group-user-info', methods=['GET', 'POST'])
def groupUserInfo():

    resp_data = {}

    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    #組id
    user_group_id = int(req['user_group_id']) if ('user_group_id' in req and req['user_group_id']) else -1
    if not user_group_id or user_group_id < 0:
        return redirect(UrlManager.buildUrl('/account/group-set'))

    query = User.query.filter(User.group_id == user_group_id)

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
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(User.uid.desc()).all()[offset:limit]
    user_group_info = UserGroup.query.filter_by(id=user_group_id).first()

    resp_data['user_group_info'] = user_group_info
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['super_admin'] = app.config['SUPER_ADMIN']
    resp_data['current'] = 'user'
    resp_data['current'] = 'account'
    resp_data['current_user'] = g.current_user

    return ops_render('account/group-user-info.html', resp_data)


@route_account.route('/group-question', methods=['GET', 'POST'])
def groupQuestion():
    resp_data = {}

    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    # 組id
    user_group_id = int(req['user_group_id']) if ('user_group_id' in req and req['user_group_id']) else -1
    if not user_group_id or user_group_id < 0:
        return redirect(UrlManager.buildUrl('/account/group-set'))

    query = Question.query.filter(Question.group_id == user_group_id)

    if 'mix_kw' in req:
        rule = or_(Question.nickname.ilike("%{0}%".format(req['mix_kw'])), Question.title.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Question.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(Question.id.desc()).all()[offset:limit]

    user_group_info = UserGroup.query.filter_by(id=user_group_id).first()

    resp_data['user_group_info'] = user_group_info
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['current'] = 'user'
    resp_data['current'] = 'account'
    resp_data['current_user'] = g.current_user
    return ops_render('account/group-question.html', resp_data)






