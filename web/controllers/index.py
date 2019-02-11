# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, g

route_index = Blueprint('index_page',__name__)

@route_index.route('/')
def index():
    current_user = g.current_user
    return render_template('index/index.html',current_user = current_user)