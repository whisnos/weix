# coding: utf-8
# from sqlalchemy import Column, DateTime, Integer, Numeric, String
# from sqlalchemy.schema import FetchedValue
from common.models import db



class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    main_image = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(10000), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    month_count = db.Column(db.Integer, nullable=False)
    total_count = db.Column(db.Integer, nullable=False)
    view_count = db.Column(db.Integer, nullable=False)
    comment_count = db.Column(db.Integer, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
