from app.extensions import db, bcrypt
from app.models.user import User


def register_user(email: str, password: str) -> User:
    """Hash password and persist new user. Raises ValueError if email taken."""
    if User.query.filter_by(email=email).first():
        raise ValueError("Email already registered.")

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate_user(email: str, password: str):
    """Return user if credentials valid, else None."""
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return user
    return None