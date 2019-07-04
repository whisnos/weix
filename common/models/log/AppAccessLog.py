# coding: utf-8
# from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Text
# from sqlalchemy.schema import FetchedValue
from common.models import db


class AppAccessLog(db.Model):
    __tablename__ = 'app_access_log'

    id = db.Column(db.Integer, primary_key=True)
    # uid = db.Column(db.BigInteger, nullable=False, index=True, )
    referer_url = db.Column(db.String(255), nullable=True,default='' )
    target_url = db.Column(db.String(255), nullable=False, )
    query_params = db.Column(db.Text, nullable=False)
    ua = db.Column(db.String(255), nullable=False, )
    ip = db.Column(db.String(32), nullable=False, )
    note = db.Column(db.String(1000), nullable=False,default='' )
    created_time = db.Column(db.DateTime, nullable=False, )
