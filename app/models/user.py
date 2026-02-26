from app.extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from app.constants.user_constants import UserConstants

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(UserConstants.MAX_EMAIL_LENGTH))
    password_hash = db.Column(db.String(UserConstants.MAX_PASSWORD_HASH_LENGTH))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    jobs = db.relationship("Job", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

