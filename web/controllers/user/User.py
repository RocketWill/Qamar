# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, request, jsonify, make_response, redirect, g
import json
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_render
from application import app, db

route_user = Blueprint('user_page', __name__)

@route_user.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')

    resp = {'code':200, 'msg':'登錄成功', 'data':{}}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '請輸入正確登入用戶名稱'
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 1:
        resp['code'] = -1
        resp['msg'] = '請輸入正確登入密碼'
        return jsonify(resp)

    user_info = User.query.filter_by(login_name = login_name).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = '請輸入正確登入用戶名或密碼'
        return jsonify(resp)

    if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = '請輸入正確登入用戶名或密碼'
        return jsonify(resp)

    response = make_response(jsonify(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],"%s#%s"%(UserService.geneAuthCode(user_info), user_info.uid))
    app.logger.info(response)


    return response



@route_user.route('/edit', methods=["GET","POST"])
def edit():
    if request.method == 'GET':
        return ops_render('user/edit.html')

    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    resp = {'code':200, 'msg':"操作成功", 'data':{}}

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = '請輸入符合規範的姓名'
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = '請輸入符合規範的郵箱'
        return jsonify(resp)

    user_info = g.current_user

    if user_info.nickname != nickname or user_info.email != email:
        user_info.nickname = nickname
        user_info.email = email
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)

    else:
        resp['code'] = -1
        resp['msg'] = '您沒有變更設置'
        return jsonify(resp)



@route_user.route('/reset-pwd')
def resetPwd():
    return ops_render('user/login.html')

@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/user/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response