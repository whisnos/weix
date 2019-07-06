# coding: utf-8
from common.models import db


class OauthAccessToken(db.Model):
    __tablename__ = 'oauth_access_token'

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(600), nullable=False)
    expired_time = db.Column(db.DateTime, nullable=False, index=True)
    created_time = db.Column(db.DateTime, nullable=False)
