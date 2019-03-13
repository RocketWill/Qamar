# -*- coding: UTF-8 -*-

from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import os
from datetime import datetime

import requests, json
from common.models.member.Member import Member
from common.models.question.Question import Question
from common.models.question.Files import File
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.libs.member.MemberService import MemberService
from common.models.reply.Reply import Reply
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class QuestionSchema(ma.ModelSchema):
    class Meta:
        model = Question


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

    member = Member.query.filter(Member.id == member_id).first()
    if not member:
        resp['code'] = -1
        resp['msg'] = "查詢不到此用戶"
        return jsonify(resp)

    current_type = int(req['current_type']) if 'current_type' in req else 0

    query = Question.query


    if current_type == 1:
        query = query.filter(Question.admin_id != 0, Question.status > 0)
    if current_type == 2:
        query = query.filter(Question.comment_count == 0)
    if current_type == 3:
        pass


    question_list = query.filter(Question.member_id == member.id).order_by(Question.updated_time.desc()).all()

    question_schema = QuestionSchema(many=True)
    question_list = question_schema.dump(question_list)







    resp['question_list'] = question_list


    return jsonify(resp)