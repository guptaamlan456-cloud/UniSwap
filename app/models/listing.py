from datetime import datetime
import json

from app import db


class Listing(db.Model):
    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    category = db.Column(db.String(80), nullable=False)
    condition = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    university = db.Column(db.String(120), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    image_url = db.Column(db.String(512), nullable=True)
    image_urls = db.Column(db.Text, nullable=True)
    free = db.Column(db.Boolean, default=False)
    urgency_level = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    seller = db.relationship("User", back_populates="listings")

    messages = db.relationship("Message", back_populates="listing", lazy="dynamic")
    chat_threads = db.relationship("ChatThread", back_populates="listing", lazy="dynamic")

    @property
    def urgency_days(self):
        if not self.departure_date:
            return None
        return (self.departure_date - datetime.utcnow().date()).days

    @property
    def urgency_label(self):
        if self.urgency_level == "very_urgent":
            return "Very urgent"
        if self.urgency_level == "medium":
            return "Medium urgency"
        if self.urgency_level == "low":
            return "Low urgency"

        days = self.urgency_days
        if days is None:
            return "No date"
        if days <= 0:
            return "Leaving soon"
        if days <= 3:
            return "High urgency"
        if days <= 7:
            return "Medium urgency"
        return "Low urgency"

    @property
    def urgency_badge_class(self):
        if self.urgency_level == "very_urgent":
            return "badge-market-danger"
        if self.urgency_level == "medium":
            return "badge-market-warning"
        if self.urgency_level == "low":
            return "badge-market-success"

        days = self.urgency_days
        if days is not None and days <= 3:
            return "badge-market-danger"
        if days is not None and days <= 7:
            return "badge-market-warning"
        return "badge-market-success"

    def get_image_urls(self):
        if not self.image_urls:
            return [self.image_url] if self.image_url else []
        try:
            urls = json.loads(self.image_urls)
            if isinstance(urls, list):
                return [u for u in urls if u]
        except Exception:
            pass
        return [self.image_url] if self.image_url else []

    def set_image_urls(self, urls):
        clean_urls = [u for u in (urls or []) if u]
        self.image_urls = json.dumps(clean_urls) if clean_urls else None
        self.image_url = clean_urls[0] if clean_urls else None
