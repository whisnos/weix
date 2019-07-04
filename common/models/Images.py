# coding: utf-8
# from sqlalchemy import Column, DateTime, Integer, String
# from sqlalchemy.schema import FetchedValue
from common.models import db


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    file_key = db.Column(db.String(60), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
