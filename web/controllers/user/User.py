# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, request, jsonify, make_response, redirect
import json
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from application import app

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



@route_user.route('/edit')
def edit():
    return render_template('user/login.html')

@route_user.route('/reset-pwd')
def resetPwd():
    return render_template('user/login.html')

@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/user/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response