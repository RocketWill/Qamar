# -*- coding: utf-8 -*-
from flask import request, g, jsonify
from common.models.log.AppAccessLog import AppAccessLog
from common.libs.Helper import getCurrentDate
from application import app, db
import json

class LogService():

    @staticmethod
    def addAccessLog():
        target = AppAccessLog()
        target.target_url = request.url
        target.referer_url = request.referrer
        target.ip = request.remote_addr
        target.query_params = json.dumps(request.values.to_dict())

        if 'current_user' in g and g.current_user is not None:
            target.uid = g.current_user.uid

        target.us = request.headers.get("User-Agent")
        target.created_time = getCurrentDate()

        db.session.add(target)
        db.session.commit()

        return True

    @staticmethod
    def addErrorLog():
        pass