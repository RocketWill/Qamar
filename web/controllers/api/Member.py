# -*- coding: UTF-8 -*-
from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import requests, json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.member.MemberService import MemberService


@route_api.route("/member/login", methods=["GET", "POST"])
def login():
    resp = {'code': 200, 'msg': "操作成功"}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "請重新登錄"
        return jsonify(resp)

    openid = MemberService.getWechatOpenid(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "請重新登錄"
        return jsonify(resp)

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''

    '''
    判斷是否已經註冊，if so 直接返回登錄頁面
    '''

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra =''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token':token}

    return jsonify(resp)


@route_api.route("/member/check-reg", methods=["POST"])
def check_reg():
    resp = {'code': 200, 'msg': "操作成功"}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "請重新登錄"
        return jsonify(resp)

    openid = MemberService.getWechatOpenid(code)

    app.logger.info(openid)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "請重新登錄"
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未綁定"
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查詢到綁定信息"
        return jsonify(resp)

    token = "%s#%s"%(MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token':token}


    return jsonify(resp)



