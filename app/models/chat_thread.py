from datetime import datetime

from app import db


class ChatThread(db.Model):
    __tablename__ = "chat_threads"

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey("listings.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    listing = db.relationship("Listing", back_populates="chat_threads")
    seller = db.relationship("User", foreign_keys=[seller_id], back_populates="seller_threads")
    buyer = db.relationship("User", foreign_keys=[buyer_id], back_populates="buyer_threads")
    messages = db.relationship("Message", back_populates="thread", lazy="dynamic")
