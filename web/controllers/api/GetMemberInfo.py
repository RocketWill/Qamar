# -*- coding: UTF-8 -*-

from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import os
from flask_marshmallow import Marshmallow
from common.models.member.Member import Member

ma = Marshmallow(app)

class MemberSchema(ma.ModelSchema):
    class Meta:
        model = Member

@route_api.route("/get-member-info", methods=["POST"])
def getMemberInfo():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    token = req['token'] if 'token' in req else ''
    if not token:
        resp['code'] = -1
        resp['msg'] = "查詢不到此用戶"
        return jsonify(resp)

    member_id = token.split("#")[1]
    if not member_id:
        resp['code'] = -1
        resp['msg'] = "查詢不到此用戶"
        return jsonify(resp)

    member = Member.query.filter_by(id = member_id).first()
    if not member:
        resp['code'] = -1
        resp['msg'] = "查詢不到此用戶"
        return jsonify(resp)

    # member_schema = MemberSchema(many=True)
    # member_info = member_schema.dump(member)

    resp['member'] = \
        {'nickname':member.nickname,
         'email_valid':member.email_validation,
         'email': member.email,
         'avatar':member.avatar
         }

    return jsonify(resp)
