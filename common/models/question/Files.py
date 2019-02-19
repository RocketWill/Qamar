# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import MEDIUMBLOB
from flask_sqlalchemy import SQLAlchemy


from application import db

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    image = db.Column(db.LargeBinary(length=2048))
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
