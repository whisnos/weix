# coding: utf-8
# from sqlalchemy import Column, DateTime, Integer, Numeric
# from sqlalchemy.schema import FetchedValue
from common.models import db


class FoodSaleChangeLog(db.Model):
    __tablename__ = 'food_sale_change_log'

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    member_id = db.Column(db.Integer, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
