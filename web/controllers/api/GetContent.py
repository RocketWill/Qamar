# -*- coding: UTF-8 -*-

from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy import or_

import requests, json
from common.models.member.Member import Member
from common.models.question.Question import Question
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.member.MemberService import MemberService
from common.models.question.QuestionCat import QuestionCat



from sqlalchemy import extract



nt=datetime.now()

ma = Marshmallow(app)

class QuestionSchema(ma.ModelSchema):
    class Meta:
        model = Question

class CatSchema(ma.ModelSchema):
    class Meta:
        model = QuestionCat

@route_api.route("/get-content", methods=["POST"])
def getContent():
    resp = {'code':200, 'msg':'操作成功', 'data':{}}
    req = request.values
    action = req['action'] if 'action' in req else ''
    active_cat_id = req['active_cat_id'] if 'active_cat_id' in req else -1
    search_kw = req['search_kw'] if 'search_kw' in req else ""
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0


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

    if search_kw:
        rule = or_(Question.content.ilike("%{0}%".format(search_kw)), Question.title.ilike("%{0}%".format(search_kw)))
        query = query.filter(rule)

    if cat_id>0:
        query = query.filter_by(cat_id=cat_id)

    resp['cat_id'] = cat_id



    # app.logger.info(query)
    list_info = query.order_by(Question.created_time.desc()).all()

    question_schema = QuestionSchema(many=True)
    ouput = question_schema.dump(list_info)

    date = nt.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
    #return jsonify(json_list=[i.serialize for i in list_info])

    categories = QuestionCat.query.all()
    cat_schema = CatSchema(many=True)
    cat = cat_schema.dump(categories)
    resp['cat'] = cat

    resp['data'] = ouput
    resp['date'] = date
    #app.logger.info(resp)



    #TEST FILTER BY MONTH
    q_time = Question.query.filter(extract('year', Question.created_time) == 2019).filter(extract('month', Question.updated_time) == 3).filter(extract('day', Question.updated_time) == 7).all()
    q_time = question_schema.dump(q_time)
    resp['q_time'] = q_time



    return jsonify(resp)



