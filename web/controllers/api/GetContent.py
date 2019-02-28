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
    active_cat_id = req['active_cat_id'] if 'active_cat_id' in req else -1

    query = Question.query
    # list = query.all()
    app.logger.info(query)

    #官方回覆過濾
    if int(active_cat_id) == 0:
        query = query.filter(Question.admin_id != 0)
    # 本週熱門過濾
    if int(active_cat_id) == 1:
        #query = query.filter(Question.admin_id != 0)
        pass
    # 尚未回覆過濾
    if int(active_cat_id) == 2:
        query = query.filter(Question.comment_count == 0)
    # 歷史火熱過濾
    if int(active_cat_id) == 3:
        query = query.filter(Question.comment_count >= 15)


    # app.logger.info(query)
    list_info = query.order_by(Question.created_time.desc()).all()

    question_schema = QuestionSchema(many=True)
    ouput = question_schema.dump(list_info)

    date = nt.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
    #return jsonify(json_list=[i.serialize for i in list_info])

    resp['data'] = ouput
    resp['date'] = date
    #app.logger.info(resp)
    return jsonify(resp)



