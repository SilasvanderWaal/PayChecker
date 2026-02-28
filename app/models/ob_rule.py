from app.extensions import db


class OBRule(db.Model):
    __tablename__ = "ob_rules"

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)

    # Period type
    period = db.Column(
        db.Enum("weekday_evening", "weekday_night", "saturday", "sunday", "public_holiday"),
        nullable=False
    )

    # User-defined time window (ignored for saturday/sunday/public_holiday full days)
    start_hour = db.Column(db.Integer, nullable=False)  # 0-23
    start_minute = db.Column(db.Integer, nullable=False, default=0)
    end_hour = db.Column(db.Integer, nullable=False)    # 0-23
    end_minute = db.Column(db.Integer, nullable=False, default=0)

    # OB supplement as percentage of hourly rate
    percentage = db.Column(db.Numeric(5, 2), nullable=False)

    def __repr__(self):
        return f"<OBRule {self.period} {self.percentage}%>"