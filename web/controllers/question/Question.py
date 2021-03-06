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
from common.models.question.QuestionCat import QuestionCat
from sqlalchemy import or_
from common.models.Image import Image
from common.models.UserGroup import UserGroup

from application import app, db

route_question = Blueprint('question_page', __name__)

@route_question.route('/index', methods=["GET","POST"])
def index():

    if request.method == "POST":
        resp = {'code': 200, 'msg':"設置成功", 'data':{}}
        req = request.values
        set_cat = req['set_cat'] if 'set_cat' in req else ''
        set_user_group = req['set_user_group'] if 'set_user_group' in req else ''

        if not set_cat and not set_user_group:
            resp['code'] = -1
            resp['msg'] = "操作失敗（可能是問題、分類或用組組信息獲取失敗）"
            return jsonify(resp)

        if set_cat:
            qid = set_cat.split("#")[1]
            cat_id = set_cat.split("#")[0]

            question = Question.query.filter_by(id=qid).first()

            if not question:
                resp['code'] = -1
                resp['msg'] = "查詢不到此問題"
                return jsonify(resp)

            #app.logger.error(question.cat_id)

            if question.cat_id == cat_id:
                resp['code'] = -1
                resp['msg'] = "無更動"
                return jsonify(resp)

            question.cat_id = cat_id
            db.session.add(question)
            db.session.commit()
            return jsonify(resp)

        if set_user_group:
            qid = set_user_group.split("#")[1]
            group_id = set_user_group.split("#")[0]

            question = Question.query.filter_by(id=qid).first()
            if not question:
                resp['code'] = -1
                resp['msg'] = "查詢不到此問題"
                return jsonify(resp)

            question.group_id = group_id
            db.session.add(question)
            db.session.commit()
            return jsonify(resp)





    # 驗證超級用戶
    if g.current_user and g.current_user.group_id > 0:
        return redirect(UrlManager.buildUrl('/account/group-set'))

    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    resp_data = {}
    resp_data['current'] = 'question'

    cat_list = QuestionCat.query.filter(QuestionCat.status != 0)
    user_group_list = UserGroup.query.filter(UserGroup.status !=0).all()

    query = Question.query

    if 'mix_kw' in req:
        rule = or_(Question.nickname.ilike("%{0}%".format(req['mix_kw'])), Question.title.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'cat_id' in req and int(req['cat_id']) > -1:
        query = query.filter(Question.cat_id == int(req['cat_id']))

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

    #return question cat




    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['cat_list'] = cat_list
    resp_data['user_group_list'] = user_group_list

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

        #驗證用戶
        if (info.group_id != admin.group_id) and admin.group_id != 0:
            return redirect(UrlManager.buildUrl('/account/group-set'))

        cat_list = QuestionCat.query.all()

        resp_data['info'] = info
        resp_data['file'] = file
        resp_data['qid'] = id
        resp_data['uid'] = admin.uid
        resp_data['cat_list'] = cat_list

        return ops_render('question/reply.html', resp_data)

    resp = {'code':200, 'msg':'回復成功', 'data':{}}
    req = request.values
    title = req['title'] if 'title' in req else ''
    content = req['content'] if 'content' in req else ''
    tags = req['tags'] if 'tags' in req else ''
    file_key = req['file'] if 'file' in req else ''

    if not content or len(content)<10:
        resp['code'] = -1
        resp['msg'] = "請輸入至少10字的回覆"
        return jsonify(resp)

    qid = req['qid'] if 'qid' in req else 0
    aid = req['aid'] if 'aid' in req else 0
    uid = req['uid'] if 'uid' in req else 0

    if int(qid) < int(1) or int(aid) < int(1):
        resp['code'] = -1
        resp['msg'] = "無法取得問題或管理員資訊"
        return jsonify(resp)

    admin = User.query.filter_by(uid = aid).first()
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
    reply_info.tags = tags
    reply_info.nickname = admin.nickname
    reply_info.aid = aid
    reply_info.uid = uid
    reply_info.qid = qid
    # reply_info.cat_id = question.cat_id
    reply_info.updated_time = reply_info.created_time = getCurrentDate()

    # if question.cat_id > 0:
    #     question_cat = QuestionCat.query.filter_by(id = cat_id).first()
    #     resp['msg'] = "已將問題分類更改成{}".format(question_cat.name)

    db.session.add(reply_info)
    db.session.commit()

    #等到管理員審核通過後才計算回覆總數
    question.reply_count = str(int(question.reply_count)+1)
    question.admin_id = aid
    #question.cat_id = reply_info.cat_id
    db.session.add(question)
    db.session.commit()

    model_image = Image()
    model_image.file_key = file_key
    model_image.rid = reply_info.id
    model_image.created_time = getCurrentDate()
    db.session.add(model_image)
    db.session.commit()

    return jsonify(resp)


@route_question.route("/all-reply")
def all_reply():
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    qid = int(req['id']) if ('id' in req and req['id']) else 0
    resp_data = {}
    resp_data['current'] = 'question'

    query = Reply.query
    question = Question.query.filter_by(id=qid).first()

    if (('mix_kw' in req) and (req['mix_kw'] != '')):
        app.logger.error("---------------"+ req['mix_kw'] +"==================")
        rule = or_(Reply.nickname.ilike("%{0}%".format(req['mix_kw'])), Reply.title.ilike("%{0}%".format(req['mix_kw'])), Reply.content.ilike("%{0}%".format(req['mix_kw'])))
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
    query = query.filter(Reply.qid == qid)
    list = query.order_by(Reply.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()


    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['question'] = question
    resp_data['qid'] = qid


    return ops_render("/question/all-reply.html",resp_data)

@route_question.route("/edit", methods=["GET","POST"])
def edit():
    if request.method == "GET":
        resp_data = {}
        resp_data['current'] = 'question'

        req = request.args
        rid = int(req.get('id', 0))

        if rid < 1:
            return redirect(UrlManager.buildUrl('/question/index'))

        reply = Reply.query.filter_by(id = rid).first()

        if not reply:
            return redirect(UrlManager.buildUrl('/question/index'))

        question = Question.query.filter_by(id = reply.qid).first()
        if not question:
            return redirect(UrlManager.buildUrl('/question/index'))

        admin = g.current_user
        # 驗證用戶
        if (question.group_id != admin.group_id) and admin.group_id != 0:
            return redirect(UrlManager.buildUrl('/account/group-set'))

        file_info = Image.query.filter_by(rid = reply.id).first()

        resp_data['info'] = reply
        resp_data['qid'] = reply.qid
        resp_data['aid'] = reply.aid
        resp_data['file'] = file_info

        return ops_render('/question/edit.html',resp_data)

    req = request.values
    resp = {'code':200,'msg':'更新成功','data':{}}
    content = req['content'] if 'content' in req else ''
    tags = req['tags'] if 'tags' in req else ''
    file_key = req['file'] if 'file' in req else ''
    if not content or len(content) < 10:
        resp['code'] = -1
        resp['msg'] = "請輸入至少10字的回覆"
        return jsonify(resp)

    qid = req['qid'] if 'qid' in req else 0
    aid = req['aid'] if 'aid' in req else 0
    rid = req['rid'] if 'rid' in req else 0

    if int(qid) < int(1) or int(aid) < int(1) or int(rid) < 1:
        resp['code'] = -1
        resp['msg'] = "無法取得問題、回覆或管理員資訊"
        return jsonify(resp)

    admin = User.query.filter_by(uid=aid).first()
    if not admin:
        resp['code'] = -1
        resp['msg'] = "無法取得管理員資訊"
        return jsonify(resp)

    question = Question.query.filter_by(id=qid).first()
    if not question:
        resp['code'] = -1
        resp['msg'] = "無法取得問題資訊"
        return jsonify(resp)

    reply = Reply.query.filter_by(id=rid).first()

    if not reply:
        resp['code'] = -1
        resp['msg'] = "無法取得先前回覆資訊"
        return jsonify(resp)

    if reply.content == content:
        resp['code'] = -1
        resp['msg'] = "內容沒有更動喔"
        return jsonify(resp)

    reply.content = content
    reply.tags = tags
    reply.updated_time = getCurrentDate()
    db.session.add(reply)
    db.session.commit()

    #每次編輯時都先刪除回復者先前上傳的檔案
    #即使檔案內容沒有更動，也回再重新上傳一次
    model_image = Image.query.filter_by(rid = reply.id).first()
    if model_image:
        db.session.delete(model_image)
        db.session.commit()

    model_image = Image()
    model_image.file_key = file_key
    model_image.rid = reply.id
    model_image.created_time = getCurrentDate()
    db.session.add(model_image)
    db.session.commit()

    return jsonify(resp)


@route_question.route("/cat")
def cat():

    # 驗證超級用戶
    if g.current_user and g.current_user.group_id > 0:
        return redirect(UrlManager.buildUrl('/account/group-set'))

    resp_data = {}
    req = request.values
    query = QuestionCat.query

    if 'status' in req and int(req['status'])> -1:
        query = query.filter(QuestionCat.status == int(req['status']))

    cat_info = query.order_by(QuestionCat.weight.desc(), QuestionCat.id.desc())

    resp_data['cat_info'] = cat_info
    resp_data['search_con'] = req
    resp_data['pages'] = ''
    resp_data['current'] = 'question'
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("/question/cat.html", resp_data)


@route_question.route("/cat-set", methods=['GET',"POST"])
def cat_set():
    if request.method == "GET":

        # 驗證超級用戶
        if g.current_user and g.current_user.group_id > 0:
            return redirect(UrlManager.buildUrl('/account/group-set'))

        resp_data = {}
        req = request.args
        cat_id = int(req.get("cat_id",0))
        cat_info = None
        if cat_id:
            cat_info = QuestionCat.query.filter_by(id = cat_id).first()
        resp_data['cat_info'] = cat_info
        resp_data['current'] = 'question'

        return ops_render("/question/cat-set.html", resp_data)

    req = request.values
    resp = {'code': 200, 'msg': '更新成功', 'data': {}}

    cat_id = req['cat_id'] if 'cat_id' in req else 0
    cat_name = req['cat_name'] if 'cat_name' in req else 0
    cat_weight = int(req['cat_weight']) if ('cat_weight' in req and int(req['cat_weight'])>0) else 1

    if cat_name == None or len(cat_name) < 2:
        resp['code'] = -1
        resp['msg'] = "請輸入符合規的分類名稱"
        return jsonify(resp)

    question_cat_info = QuestionCat.query.filter_by(id=cat_id).first()

    if question_cat_info:
        model_question_cat = question_cat_info
    else:
        model_question_cat = QuestionCat()
        model_question_cat.created_time = getCurrentDate()

    model_question_cat.name = cat_name
    model_question_cat.weight = cat_weight
    model_question_cat.updated_time = getCurrentDate()

    db.session.add(model_question_cat)
    db.session.commit()
    return jsonify(resp)



@route_question.route("/cat-ops", methods=["POST"])
def catOps():
    resp = {'code':200,"msg":"操作成功","data":{}}
    req = request.values
    cat_id = req['cat_id'] if 'cat_id' in req else 0
    act = req['act'] if 'act' in req else ''

    if not cat_id:
        resp['code'] = -1
        resp['msg'] = "查詢不到此問題分類"
        return jsonify(resp)

    question_cat_info = QuestionCat.query.filter_by(id = cat_id).first()
    if not question_cat_info:
        resp['code'] = -1
        resp['msg'] = "查詢不到此問題分類"
        return jsonify(resp)

    if act not in ["remove","recover"]:
        resp['code'] = -1
        resp['msg'] = "無法執行此操作"
        return jsonify(resp)

    if act == "remove":
        question_cat_info.status = 0

    if act == "recover":
        question_cat_info.status = 1

    db.session.add(question_cat_info)
    db.session.commit()
    return jsonify(resp)











