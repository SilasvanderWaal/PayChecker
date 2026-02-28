from app.extensions import db
from datetime import datetime
from app.constants.job_constatns import JobConstants as const

class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(const.MAX_NAME_LENGTH), nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(const.MAX_CURRENCY_NAME_LENGTH), default="SEK")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shifts = db.relationship("Shift", backref="job", lazy=True)

    def __repr__(self):
        return f"<Job {self.name}>"