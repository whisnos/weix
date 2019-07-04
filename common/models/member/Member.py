# coding: utf-8
# from sqlalchemy import Column, DateTime, Integer, String
# from sqlalchemy.schema import FetchedValue

from common.models import db

class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(11), nullable=True)
    sex = db.Column(db.Integer, nullable=False)
    avatar = db.Column(db.String(200), nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    reg_ip = db.Column(db.String(100), nullable=True)
    status = db.Column(db.Integer, nullable=False,default=1)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)

    @property
    def status_desc(self):
        from application import app
        return app.config['STATUS_MAPPING'][str(self.status)]

    @property
    def sex_desc(self):
        SEX_MAPPING={
            '0':'未知',
            '1': '男',
            '2': '女',
        }
        return SEX_MAPPING[str(self.sex)]