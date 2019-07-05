# coding: utf-8
# from sqlalchemy import Column, DateTime, Integer, String
# from sqlalchemy.schema import FetchedValue

from common.models import db


class FoodCat(db.Model):
    __tablename__ = 'food_cat'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False,default=1)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)

    @property
    def status_desc(self):
        from application import app
        return app.config['STATUS_MAPPING'][str(self.status)]
