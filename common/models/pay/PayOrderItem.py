# coding: utf-8
from common.models import db


class PayOrderItem(db.Model):
    __tablename__ = 'pay_order_item'

    id = db.Column(db.Integer, primary_key=True)
    pay_order_id = db.Column(db.Integer, nullable=False, index=True)
    member_id = db.Column(db.BigInteger, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    food_id = db.Column(db.Integer, nullable=False, index=True)
    note = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=True)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
