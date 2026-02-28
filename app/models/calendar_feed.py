from app.extensions import db
from datetime import datetime

class CalendarFeed(db.Model):
    __tablename__ = "calendar_feeds"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    url = db.Column(db.String(2048), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    last_synced_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    job = db.relationship("Job", backref="calendar_feeds")

    def __repr__(self):
        return f"<CalendarFeed {self.name}>"