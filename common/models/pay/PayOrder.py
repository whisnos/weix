# coding: utf-8
from common.models import db


class PayOrder(db.Model):
    __tablename__ = 'pay_order'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    order_sn = db.Column(db.String(40), nullable=False, unique=True)
    member_id = db.Column(db.BigInteger, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    yun_price = db.Column(db.Numeric(10, 2), nullable=False)
    pay_price = db.Column(db.Numeric(10, 2), nullable=False)
    pay_sn = db.Column(db.String(128), nullable=True)
    prepay_id = db.Column(db.String(128), nullable=True)
    note = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer, nullable=False)
    express_status = db.Column(db.Integer, nullable=False)
    express_address_id = db.Column(db.Integer, nullable=False)
    express_info = db.Column(db.String(200), nullable=True)
    comment_status = db.Column(db.Integer, nullable=True)
    pay_time = db.Column(db.DateTime, nullable=True)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)


    @property
    def pay_status(self):
        tmp_status = self.status
        if self.status == 1:
            tmp_status = self.express_status
            if self.express_status == 1 and self.comment_status == 0:
                tmp_status = -5
            if self.express_status == 1 and self.comment_status == 1:
                tmp_status = 1
        return tmp_status

    @property
    def status_desc(self):
        return app.config['PAY_STATUS_DISPLAY_MAPPING'][ str( self.pay_status )]

    @property
    def order_number(self):
        order_number = self.created_time.strftime("%Y%m%d%H%M%S")
        order_number = order_number + str(self.id).zfill(5)
        return order_number
