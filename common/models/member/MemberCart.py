# coding: utf-8
from common.models import db


class MemberCart(db.Model):
    __tablename__ = 'member_cart'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.BigInteger, nullable=False, index=True)
    food_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
