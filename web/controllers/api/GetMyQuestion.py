# -*- coding: UTF-8 -*-

from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import os
from flask_marshmallow import Marshmallow
from datetime import datetime

import requests, json
from common.models.member.Member import Member
from common.models.question.Question import Question
from common.models.question.Files import File
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.libs.member.MemberService import MemberService
from common.models.reply.Reply import Reply


@route_api.route("/get-my-question", methods=["POST"])
def getMyQuestion():
    resp = {'code':200,'msg':'操作成功','data':{}}
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

    # Member = Reply.query.filter_by()




    resp['req'] = req

    return jsonify(resp)