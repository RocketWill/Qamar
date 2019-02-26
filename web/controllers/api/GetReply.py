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
from common.models.reply.Reply import Reply
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.libs.member.MemberService import MemberService
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class ReplySchema(ma.ModelSchema):
    class Meta:
        model =Reply


@route_api.route("/get-reply", methods=["GET", "POST"])
def getReply():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    qid = int(req['qid']) if 'qid' in req else 0

    if qid < 1:
        resp['code'] = -1
        resp['msg'] = "無法取得問題信息"
        return jsonify(resp)

    resp['qid'] = qid

    reply_info = Reply.query.filter_by(qid=qid).order_by(Reply.updated_time.desc()).all()
    if not reply_info:
        resp['code'] = -1
        resp['msg'] = "無法取得回覆信息"
        return jsonify(resp)


    reply_schema = ReplySchema(many=True)
    output = reply_schema.dump(reply_info)
    app.logger.error(output)
    #app.logger.error(json.loads(output))
    resp['data'] = output



    return jsonify(resp)




