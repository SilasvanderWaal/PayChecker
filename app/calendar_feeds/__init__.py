from flask import Blueprint

calendar_feeds_bp = Blueprint("calendar_feeds", __name__, url_prefix="/calendar-feeds")

from app.calendar_feeds import routes