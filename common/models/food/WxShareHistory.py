# coding: utf-8
from common.models import db


class WxShareHistory(db.Model):
    __tablename__ = 'wx_share_history'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, nullable=False)
    share_url = db.Column(db.String(200), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
