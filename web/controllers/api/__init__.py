# -*- coding: UTF-8 -*-
from flask import Blueprint

route_api = Blueprint('api_page', __name__)

from web.controllers.api.Member import *
from web.controllers.api.GetContent import *
from web.controllers.api.GetQuestion import *
from web.controllers.api.GetMyQuestion import *
from web.controllers.api.GetReply import *
@route_api.route("/")
def index():
    return "Mina Api V1.0"