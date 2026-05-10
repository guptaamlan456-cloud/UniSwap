from datetime import datetime

from app import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey("listings.id"), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey("chat_threads.id"), nullable=True)

    sender = db.relationship("User", back_populates="messages")
    listing = db.relationship("Listing", back_populates="messages")
    thread = db.relationship("ChatThread", back_populates="messages")
