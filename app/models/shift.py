from app.extensions import db
from datetime import datetime


class Shift(db.Model):
    __tablename__ = "shifts"

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    source = db.Column(db.Enum("manual", "ics"), default="manual", nullable=False)
    break_duration = db.Column(db.Integer, default=0, nullable=False)
    ics_uid = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "ics_uid", name="uq_user_ics_uid"),
    )

    @property
    def duration_hours(self):
        """Return shift duration as a float in hours."""
        delta = self.end_time - self.start_time
        total_minutes = (delta.total_seconds() / 60) - self.break_duration 
        return max(total_minutes, 0) / 60

    def __repr__(self):
        return f"<Shift {self.id} {self.start_time}>"
