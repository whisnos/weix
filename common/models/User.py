# coding: utf-8
# from sqlalchemy import BigInteger, Column, DateTime, Integer, String
# from sqlalchemy.schema import FetchedValue
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
# 注释掉上面的db 换成我们的
from common.models import db


class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.BigInteger, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.Integer, nullable=True)
    avatar = db.Column(db.String(64), nullable=True)
    login_name = db.Column(db.String(20), nullable=False, unique=True)
    login_pwd = db.Column(db.String(32), nullable=False)
    login_salt = db.Column(db.String(32), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
