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
from common.libs.member.MemberService import MemberService


@route_api.route("/get-question", methods=["POST"])
def getQuestion():
    resp = {'code':200, 'msg':'操作成功', 'data':{}}

    f = request.files['shit'] if 'shit' in request.files else ''
    app.logger.info(f)
    req = request.values

    title = req['title'] if 'title' in req else ''
    content = req['content'] if 'content' in req else ''
    token = req['token'] if 'token' in req else ''

    uid = token.split("#")[1]

    if not uid:
        resp['code'] = -1
        resp['msg'] = 'error'
        return jsonify(resp)

    member_info = Member.query.filter_by(id=uid).first()

    if not member_info:
        resp['code'] = -1
        resp['msg'] = 'error'
        return jsonify(resp)

    question = Question()
    question.member_id = uid
    question.title = title
    question.content = content
    question.created_time = question.updated_time = getCurrentDate()

    db.session.add(question)
    db.session.commit()

    if f:
        # user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        src_imgname = str(question.id) + ".jpg"
        upload_path = os.path.join(basepath, 'static/srcImg/')

        app.logger.info(basepath)

        if os.path.exists(upload_path) == False:
            os.makedirs(upload_path)
        f.save(upload_path + src_imgname)




    # im = cv2.imread(upload_path + src_imgname, 0)
    # save_path = os.path.join(basepath, 'static/resImg/')
    # if os.path.exists(save_path) == False:
    #     os.makedirs(save_path)
    # save_imgname = str(uuid.uuid1()) + ".jpg"
    # cv2.imwrite(save_path + save_imgname, im)
    # resSets["value"] = 10
    # resSets["resurl"] = "http://127.0.0.1:8090" + '/static/resImg/' + save_imgname

    return jsonify(resp)

