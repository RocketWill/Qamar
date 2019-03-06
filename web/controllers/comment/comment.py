# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, g, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.models.log.AppAccessLog import AppAccessLog
from common.libs.UrlManager import UrlManager
from common.models.member.Member import Member
from common.models.comment.Comment import Comment
from common.models.question.Question import Question
from sqlalchemy import or_

from application import app, db

route_comment = Blueprint('comment_page', __name__)

@route_comment.route('/index')
def index():
    resp_data = {}
    req = request.values
    qid = int(req['qid']) if 'qid' in req else 0
    page = int(req['p']) if ('p' in req and req['p']) else 1


    question = Question.query.filter_by(id=qid).first()

    if not question:
        return redirect(UrlManager.buildUrl('/question/index'))

    query = Comment.query

    if 'mix_kw' in req:
        rule = or_(Comment.nickname.ilike("%{0}%".format(req['mix_kw'])), Comment.content.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Comment.status == int(req['status']))



    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page),"")
    }

    pages = iPagination(page_params)
    offset = (page -1) * app.config['PAGE_SIZE']
    comment_list = query.filter_by(qid=qid).order_by(Comment.created_time.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] ='question'

    resp_data['question'] = question
    resp_data['comment_list'] = comment_list
    return ops_render('./comment/index.html', resp_data)

@route_comment.route('/ops', methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': "操作成功", "data": {}}
    req = request.values

    cid = int(req['cid']) if 'cid' in req else 0
    act = req['act'] if 'act' in req else ""
    qid = int(req['qid']) if 'qid' in req else 0

    if cid < 1:
        resp['code'] = -1
        resp['msg'] = "請選擇要操作的意見"
        return jsonify(resp)

    if qid < 1:
        resp['code'] = -1
        resp['msg'] = "查詢不到該意見對應的問題"
        return jsonify(resp)

    if act not in ["remove", "recover"]:
        resp['code'] = -1
        resp['msg'] = '操作有誤，請重試'
        return jsonify(resp)

    comment_info = Comment.query.filter_by(id=cid).first()

    if not comment_info:
        resp['code'] = -1
        resp['msg'] = '查無此意見，請重試'
        return jsonify(resp)

    question = Question.query.filter_by(id=qid).first()
    if act == "remove":
        comment_info.status = 0
        question.discuss_count = question.discuss_count - 1
    elif act == "recover":
        comment_info.status = 1
        question.discuss_count = question.discuss_count + 1

    db.session.add(comment_info, question)
    db.session.commit()

    return jsonify(resp)
