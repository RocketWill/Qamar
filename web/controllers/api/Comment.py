# -*- coding: UTF-8 -*-

from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
from flask_marshmallow import Marshmallow

import requests, json
from common.models.member.Member import Member
from common.models.question.Question import Question
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.member.MemberService import MemberService
from common.models.comment.Comment import Comment

@route_api.route("/post-comment", methods=["POST"])
def postComment():
    resp = {'code':200, 'msg':"操作成功", "data":{}}
    req = request.values

    qid = int(req['qid']) if 'qid' in req else 0
    comment = req['comment'] if 'comment' in req else ''
    token = req['token'] if 'token' in req else ''

    question = Question.query.filter_by(id=qid).first()
    if not question:
        resp['code'] = -1
        resp['msg'] = "抱歉，查無此問題信息，請稍候重試"
        return jsonify(resp)


    if not token:
        resp['code'] = -1
        resp['msg'] = "抱歉，系統無法確認您的使用者身份，若此問題持續出現，請聯繫學校管理員，謝謝！"
        return jsonify(resp)

    uid = token.split("#")[1]
    if not uid:
        resp['code'] = -1
        resp['msg'] = "抱歉，系統無法確認您的使用者身份，若此問題持續出現，請聯繫學校管理員，謝謝！"
        return jsonify(resp)

    member = Member.query.filter_by(id=uid).first()
    if not member:
        resp['code'] = -1
        resp['msg'] = "抱歉，系統無法確認您的使用者身份，若此問題持續出現，請聯繫學校管理員，謝謝！"
        return jsonify(resp)

    if member.email_validation != 1:
        resp['code'] = 300
        resp['msg'] = "看來您還沒有進行郵箱驗證喔，驗證後就可以使用「Qamar 卡碼」的所有完整功能啦！"
        return jsonify(resp)

    if not comment:
        resp['code'] = -1
        resp['msg'] = "抱歉，無法取的您的意見信息，請稍候重試"
        return jsonify(resp)


    comment_info = Comment()
    comment_info.qid = qid
    comment_info.uid = member.id
    comment_info.content = comment
    comment_info.created_time = getCurrentDate()
    comment_info.nickname = member.nickname
    db.session.add(comment_info)
    db.session.commit()

    question.discuss_count = question.discuss_count + 1
    db.session.add(question)
    db.session.commit()

    return jsonify(resp)
