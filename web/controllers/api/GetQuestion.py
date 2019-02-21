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
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.libs.member.MemberService import MemberService


@route_api.route("/get-question", methods=["POST"])
def getQuestion():
    resp = {'code':200, 'msg':'操作成功', 'data':{}}

    f = request.files['post-question'] if 'post-question' in request.files else ''
    app.logger.info(f)
    req = request.values

    app.logger.info(req)

    title = req['title'] if 'title' in req else ''
    content = req['content'] if 'content' in req else ''
    anony = req['anony'] if 'anony' in req else ''
    random_str = req['random_str'] if 'random_str' in req else ''
    token = req['token'] if 'token' in req else ''

    if title==None or len(title)<10 or content == None or len(content)<20:
        resp['code'] = -1
        resp['msg'] = "請確認內容符合字數規範，稍後重試"
        return jsonify(resp)

    if token==None or len(token)<1:
        resp['code'] = -1
        resp['msg'] = "無法獲取用戶信息，稍後重試"
        return jsonify(resp)

    if anony == 'true':
        anony = 0
    else:
        anony = 1

    uid = token.split("#")[1]

    if not uid:
        resp['code'] = -1
        resp['msg'] = 'error'
        return jsonify(resp)

    member_info = Member.query.filter_by(id=uid).first()

    if member_info.email_validation != 1:
        resp['code'] = 300
        resp['msg'] = "需先進行郵箱認證才能使用發問功能。若無法驗證成功，請聯繫管理員進行人工驗證。"
        return jsonify(resp)

    if not member_info:
        resp['code'] = -1
        resp['msg'] = 'error'
        return jsonify(resp)

    hasIn = File.query.filter_by(salt=random_str).first()
    if hasIn:
        question = Question.query.filter_by(id=hasIn.qid).first()
        if not question:
            app.logger.error("no find")
        else:
            app.logger.error("find!!!!!!!!!!!!!!")
            app.logger.error("--------"+str(question.id))


    if not hasIn:
        question = Question()
        question.member_id = uid
        question.title = title
        question.content = content
        question.public = anony
        if anony == 1:
            question.nickname = member_info.nickname
        else:
            question.nickname = "匿名"
        question.created_time = question.updated_time = getCurrentDate()

        db.session.add(question)
        db.session.commit()




    if f:
        # user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        basepath2 = os.path
        app.logger.info(basepath2)


        #src_imgname = str(question.id) + ".jpg"
        src_imgname = UserService.geneSalt(10) + ".jpg"
        upload_path = os.path.join('web/static/upload/')

        app.logger.info(basepath)

        if os.path.exists(upload_path) == False:
            os.makedirs(upload_path)
        f.save(upload_path + src_imgname)

        file_info = File()
        file_info.qid = question.id
        file_info.created_time = getCurrentDate()
        file_info.image = f.read()
        file_info.salt = random_str
        file_info.path = "static/upload/" + src_imgname

        db.session.add(file_info)
        db.session.commit()





    # im = cv2.imread(upload_path + src_imgname, 0)
    # save_path = os.path.join(basepath, 'static/resImg/')
    # if os.path.exists(save_path) == False:
    #     os.makedirs(save_path)
    # save_imgname = str(uuid.uuid1()) + ".jpg"
    # cv2.imwrite(save_path + save_imgname, im)
    # resSets["value"] = 10
    # resSets["resurl"] = "http://127.0.0.1:8090" + '/static/resImg/' + save_imgname

    return jsonify(resp)

