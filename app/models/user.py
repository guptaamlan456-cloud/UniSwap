from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(120), nullable=True)
    university = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    listings = db.relationship("Listing", back_populates="seller", lazy="dynamic")
    messages = db.relationship("Message", back_populates="sender", lazy="dynamic")
    seller_threads = db.relationship(
        "ChatThread",
        foreign_keys="ChatThread.seller_id",
        back_populates="seller",
        lazy="dynamic",
    )
    buyer_threads = db.relationship(
        "ChatThread",
        foreign_keys="ChatThread.buyer_id",
        back_populates="buyer",
        lazy="dynamic",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
