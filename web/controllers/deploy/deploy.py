# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, g, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.models.log.AppAccessLog import AppAccessLog
from common.libs.UrlManager import UrlManager
from common.models.User import User
from common.models.UserGroup import UserGroup
from common.models.question.Question import Question
from common.models.question.QuestionCat import QuestionCat
from common.models.reply.Reply import Reply

from sqlalchemy import or_

from application import app, db

route_deploy = Blueprint('deploy_page', __name__)


@route_deploy.route('/index')
def index():
    resp = {}

    user_group_list = UserGroup.query.filter_by(status=1).order_by(UserGroup.weight.desc()).all()
    question_list = Question.query.filter(Question.comment_count > 0).order_by(Question.updated_time.desc())
    cat_list = QuestionCat.query.filter_by(status=1).order_by(QuestionCat.weight.desc()).all()


    resp['current'] = 'deploy'
    resp['user_group_list'] = user_group_list
    resp['question_list'] = question_list
    resp['cat_list'] = cat_list
    return ops_render("deploy/index.html",resp)

@route_deploy.route('/review', methods=["GET", "POST"])
def review():
    if request.method == "GET":
        resp = {}
        req = request.values
        question_id = int(req['qid']) if ('qid' in req) else 0

        if question_id < 1:
            return redirect(UrlManager.buildUrl('/deploy/index'))

        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return redirect(UrlManager.buildUrl('/deploy/index'))

        reply_list = Reply.query.filter_by(qid=question_id).order_by(Reply.updated_time.desc()).all()

        app.logger.error(reply_list)

        resp['current'] = 'deploy'
        resp['reply_list'] = reply_list
        resp['question'] = question
        return ops_render("deploy/review.html", resp)


    resp = {'code':200, 'msg':'設置成功', 'data':{}}
    req = request.values
    set_review = req['set_review'] if 'set_review' in req else ''
    if not set_review:
        resp['code'] = -1
        resp['msg'] = '無法辨識此操作，請稍後再試'
        return jsonify(resp)

    reply_id = int(set_review.split('#')[1])
    action = int(set_review.split('#')[0])  # 0:禁止發布; 1: 只限發問人; 2: 公開

    reply = Reply.query.filter_by(id=reply_id).first()

    if not reply:
        resp['code'] = -1
        resp['msg'] = '查無此回覆'
        return jsonify(resp)

    question = Question.query.filter_by(id = reply.qid).first()
    if not question:
        resp['code'] = -1
        resp['msg'] = '查無此回覆對應之問題'
        return jsonify(resp)

    if action == 0:
        reply.status = 0
    elif action == 1:
        reply.status = 1
        question.status = 1
        db.session.add(question)
        db.session.commit()
    elif action == 2:
        reply.status = 2
        question.status = 2
        db.session.add(question)
        db.session.commit()

    reply.updated_time = getCurrentDate()
    db.session.add(reply)
    db.session.commit()
    return jsonify(resp)

