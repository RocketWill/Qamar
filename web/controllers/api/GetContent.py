# -*- coding: UTF-8 -*-

from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
from flask_marshmallow import Marshmallow
from datetime import datetime

import requests, json
from common.models.member.Member import Member
from common.models.question.Question import Question
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.member.MemberService import MemberService
nt=datetime.now()

ma = Marshmallow(app)

class QuestionSchema(ma.ModelSchema):
    class Meta:
        model = Question

@route_api.route("/get-content", methods=["POST"])
def getContent():
    resp = {'code':200, 'msg':'操作成功', 'data':{}}
    req = request.values
    action = req['action'] if 'action' in req else ''


    query = Question.query
    # list = query.all()
    app.logger.info(query)

    # app.logger.info(query)
    list_info = Question.query.order_by(Question.created_time.desc()).all()

    question_schema = QuestionSchema(many=True)
    ouput = question_schema.dump(list_info)

    date = nt.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
    #return jsonify(json_list=[i.serialize for i in list_info])

    resp['data'] = ouput
    resp['date'] = date
    #app.logger.info(resp)
    return jsonify(resp)



