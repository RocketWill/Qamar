# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy
from application import app, db


class Reply(db.Model):
    __tablename__ = 'reply'

    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    uid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    aid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    cat_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    title = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.String(10000), nullable=False, server_default=db.FetchedValue())
    tags = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
