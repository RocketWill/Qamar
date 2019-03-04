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
from common.models.reply.Reply import Reply
from common.models.Image import Image
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.libs.member.MemberService import MemberService
from flask_marshmallow import Marshmallow
from sqlalchemy import or_


ma = Marshmallow(app)

class ImageSchema(ma.ModelSchema):
    class Meta:
        model = Image

class ReplySchema(ma.ModelSchema):
    #image = ma.Nested(ImageSchema, many=True)
    class Meta:
        model =Reply

class MSchema(ma.ModelSchema):
    reply = ma.Nested(ReplySchema)
    image = ma.Nested(ImageSchema)

MSchema = MSchema(many=True)


@route_api.route("/get-reply", methods=["GET", "POST"])
def getReply():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    qid = int(req['qid']) if 'qid' in req else 0

    if qid < 1:
        resp['code'] = -1
        resp['msg'] = "無法取得問題信息"
        return jsonify(resp)

    resp['qid'] = qid

    reply_info = Reply.query.filter_by(qid=qid).order_by(Reply.updated_time.desc()).all()

    reply_info_add_file = db.session.query(Reply, Image).filter(Reply.qid==qid).join(Image, Image.rid == Reply.id).all()
    # reply_info_add_file = db.session.query(Reply, Image)\
    #     .filter(or_(Image.rid==Reply.id, Image.rid==0))\
    #     .filter(Reply.qid == qid)\
    #     .all()


    app.logger.error(reply_info_add_file)



    if not reply_info:
        resp['code'] = -1
        resp['msg'] = "無法取得回覆信息"
        return jsonify(resp)


    reply_schema = ReplySchema(many=True)
    image_schema = ImageSchema(many=True)
    output = reply_schema.dump(reply_info)
    #app.logger.error(output)
    #app.logger.error(json.loads(output))
    resp['data'] = output

    reply = MSchema.dump([{'reply': x[0], 'image': x[1]} for x in reply_info_add_file])

    # #reply = MSchema.dump([[x[0],x[1]] for x in reply_info_add_file])
    #
    # reply = []
    # img = []
    # for x in reply_info_add_file:
    #     # reply.append(MSchema.dump(x[0]))
    #     # reply.append(MSchema.dump(x[1]))
    #     reply.append(x[0])
    #     reply.append(x[1])
    #
    # app.logger.error(reply)

    #eply = MSchema.dump([x for x in reply])


    output_file = []




    resp['data_file'] = reply
    #resp['data_image'] = image



    return jsonify(resp)




