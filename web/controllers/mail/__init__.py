# -*- coding: UTF-8 -*-
from application import app, db
from flask_mail import Mail, Message
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from flask import Blueprint, render_template, request, redirect, jsonify, g, url_for, session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, TimedJSONWebSignatureSerializer
from common.libs.user.UserService import UserService
from common.models.member.Member import Member

mail = Mail(app)
route_mail = Blueprint('mail_validation', __name__)

s = URLSafeTimedSerializer('Thisisasecret')
salt = UserService.geneSalt()
member_id = "0"


@route_mail.route('/validation', methods=["GET","POST"])
def mail_validation():
    if request.method == "GET":
        resp_data = {}
        resp_data['current_user'] = ''

        g.email = None
        if request.method == "GET":
            if g.email:
                resp_data['email'] = g.email



    req = request.values
    email = req['email'] if 'email' in req else ''
    email = email+app.config['EMAIL_POSTFIX']
    token = req['key'] if 'key' in req else ''
    resp = {'code': 200, 'msg': "已將驗證鏈接發送至{}。請點擊郵箱中的鏈接以啟用「Qamar 卡碼」完整功能".format(email)}
    if not token:
        resp['code'] = -1
        resp['msg'] = "驗證用戶失敗，請重試"
        return jsonify(resp)

    member_id = token.split("#")[1]
    member_info = Member.query.filter_by(id=member_id).first()
    if not member_info:
        resp_data['title'] = "查無該使用者"
        resp_data['info'] = "請稍後再次嘗試"
        return jsonify(resp)

    member_info.email = email
    db.session.add(member_info)
    db.session.commit()
    #
    # resp['email'] = email
    # resp['member_id'] = member_id

    #g.email = None
    token = s.dumps(email, salt=salt)


    try:
        msg = Message('Comfirm Email', sender='will.chengyong@gmail.com', recipients=[email])
        link=url_for('mail_validation.comfirm',token=token,id=member_id, _external=True)
        app.logger.info(link)
        msg.body = 'Your link is {}'.format(link)
        #msg.body = "hello"
        app.logger.info(msg)
        mail.send(msg)
        return jsonify(resp)
    except:
        resp['code'] = -1
        resp['msg'] = "發送郵件時遇到問題，請稍候重試"
        return jsonify(resp)


    app.logger.info(email)
    #resp['msg'] = email
    # resp['token'] = token
    # g.email = mail

    return jsonify(resp)


@route_mail.route('/comfirm/<id>/<token>', methods=["GET","POST"])
def comfirm(token, id):
    resp_data = {'title':"恭喜！郵箱驗證成功","info":"您已可以使用「Qamar 卡碼」完整功能"}
    #req = request.args
    #id = int(req.get('id', 0))


    try:
        email = s.loads(token, salt=salt, max_age=100)
    except SignatureExpired:
        resp_data['title'] = "鏈接已逾期"
        resp_data['info'] = "請稍後再嘗試一次"
        return ops_render("mail/email-validation.html", resp_data)

    #app.logger.info(id)
    member_info = Member.query.filter_by(id=id).first()
    if not member_info:
        resp_data['title'] = "查無該使用者"
        resp_data['info'] = "請稍後再次嘗試"
        return ops_render("mail/email-validation.html", resp_data)

    if member_info.email_validation == 0:
        member_info.email_validation = 1

        db.session.add(member_info)
        db.session.commit()
    else:
        resp_data['title'] = "您已啟用過郵箱驗證"
        resp_data['info'] = "請返回「Qamar 卡碼」體驗完整功能"
        return ops_render("mail/email-validation.html", resp_data)


    return ops_render("mail/email-validation.html", resp_data)
