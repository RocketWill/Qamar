# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, g, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.models.log.AppAccessLog import AppAccessLog
from common.libs.UrlManager import UrlManager
from common.models.member.Member import Member
from sqlalchemy import or_
from common.models.question.Files import File
import base64

from application import app, db

route_image = Blueprint('image_page', __name__)

@route_image.route('/index')
def index():
    resp_data = {}
    ds = File.query.all()
    resp_data['ds'] = ds
    resp_data['base64'] = base64

    return ops_render('image/image.html', resp_data)
