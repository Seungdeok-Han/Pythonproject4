from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Numeric
from datetime import datetime
from sqlalchemy.dialects.mysql import JSON

class BrandInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    origin_country = db.Column(db.String(100))
    famous_users = db.Column(db.Text)
    logo_url = db.Column(db.String(255))

class InstrumentPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand_info.id'))
    model_name = db.Column(db.String(100))
    shape = db.Column(db.String(100))
    condition = db.Column(db.Integer)  # 0~100
    description = db.Column(db.Text)
    price = db.Column(Numeric(10, 2))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # FK로 연결
    user = db.relationship('User', backref='posts')  # 관계 설정
    brand = db.relationship('BrandInfo')
    images = db.Column(JSON)  # 이미지 파일명
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='available')  # 거래 상태: available, reserved, sold

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    likes = db.relationship('Like', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('instrument_post.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    replies = db.relationship('Comment',
                              backref=db.backref('parent', remote_side=[id]),
                              lazy='dynamic')

    user = db.relationship('User', backref='comments')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('instrument_post.id'), nullable=False)

    user = db.relationship('User', overlaps="likes")
    post = db.relationship('InstrumentPost', backref=db.backref('likes', cascade='all, delete-orphan'))

class MyInstrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    images = db.Column(JSON)  # 여러장
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='my_instruments')

class GenreTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    genres = db.Column(db.String(200), nullable=False)  # 쉼표로 구분된 장르 문자열
    __table_args__ = (db.UniqueConstraint('brand', 'model_name', name='uix_brand_model'),)
