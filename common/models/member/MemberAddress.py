# coding: utf-8
from common.models import db


class MemberAddress(db.Model):
    __tablename__ = 'member_address'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    mobile = db.Column(db.String(11), nullable=False)
    province_id = db.Column(db.Integer, nullable=False)
    province_str = db.Column(db.String(50), nullable=False)
    city_id = db.Column(db.Integer, nullable=False)
    city_str = db.Column(db.String(50), nullable=False)
    area_id = db.Column(db.Integer, nullable=False)
    area_str = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False,default=1)
    is_default = db.Column(db.Integer, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
