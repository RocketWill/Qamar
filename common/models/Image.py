# coding: utf-8
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from application import app, db


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    file_key = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
