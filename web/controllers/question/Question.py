# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, g, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.models.member.Member import Member
from common.models.question.Question import Question
from common.models.question.QuestionCat import QuestionCat
from common.models.question.Files import File
from common.models.User import User
from common.models.reply.Reply import Reply
from sqlalchemy import or_

from application import app, db

route_question = Blueprint('question_page', __name__)

@route_question.route('/index')
def index():
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    resp_data = {}
    resp_data['current'] = 'question'

    query = Question.query

    if 'mix_kw' in req:
        rule = or_(Question.nickname.ilike("%{0}%".format(req['mix_kw'])), Question.title.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Member.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    list = query.order_by(Question.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()


    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req


    return ops_render('question/index.html',resp_data)


@route_question.route("/reply", methods=['GET','POST'])
def reply():

    if request.method == "GET":
        resp_data = {}
        resp_data['current'] = 'question'
        resp_data['search_con'] = ''
        req = request.args
        id = int(req.get('id', 0))
        if id < 1:
            return redirect(UrlManager.buildUrl('/question/index'))

        info = Question.query.filter_by(id=id).first()
        if not info:
            return redirect(UrlManager.buildUrl('/question/index'))

        file = File.query.filter_by(qid=info.id)

        admin = g.current_user
        if not admin:
            return redirect(UrlManager.buildUrl('/question/index'))

        resp_data['info'] = info
        resp_data['file'] = file
        resp_data['qid'] = id
        resp_data['uid'] = admin.uid

        return ops_render('question/reply.html', resp_data)

    resp = {'code':200, 'msg':'回復成功', 'data':{}}
    req = request.values
    title = req['title'] if 'title' in req else ''
    content = req['content'] if 'content' in req else ''
    if not content or len(content)<10:
        resp['code'] = -1
        resp['msg'] = "請輸入至少10字的回覆"
        return jsonify(resp)

    qid = req['qid'] if 'qid' in req else 0
    uid = req['uid'] if 'uid' in req else 0

    if int(qid) < int(1) or int(uid) < int(1):
        resp['code'] = -1
        resp['msg'] = "無法取得問題或管理員資訊"
        return jsonify(resp)

    admin = User.query.filter_by(uid = uid).first()
    if not admin:
        resp['code'] = -1
        resp['msg'] = "無法取得管理員資訊"
        return jsonify(resp)

    question = Question.query.filter_by(id=qid).first()
    if not question:
        resp['code'] = -1
        resp['msg'] = "無法取得問題資訊"
        return jsonify(resp)

    reply_info = Reply()
    reply_info.title = title
    reply_info.content = content
    reply_info.nickname = admin.nickname
    reply_info.uid = uid
    reply_info.qid = qid
    reply_info.cat_id = question.cat_id
    reply_info.updated_time = reply_info.created_time = getCurrentDate()

    db.session.add(reply_info)
    db.session.commit()

    return jsonify(resp)
