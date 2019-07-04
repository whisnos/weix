# coding: utf-8
# from sqlalchemy import Column, DateTime, Integer, String, Text
# from sqlalchemy.schema import FetchedValue
from common.models import db


class AppErrorLog(db.Model):
    __tablename__ = 'app_error_log'

    id = db.Column(db.Integer, primary_key=True)
    referer_url = db.Column(db.String(255), nullable=True, )
    target_url = db.Column(db.String(255), nullable=False, )
    query_params = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, )
