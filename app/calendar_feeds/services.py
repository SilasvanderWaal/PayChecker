import requests
from datetime import datetime, timezone

from app.extensions import db
from app.models.calendar_feed import CalendarFeed
from app.models.job import Job
from app.shifts.services import import_shifts_from_ics


def get_user_feeds(user_id: int):
    return (
        CalendarFeed.query
        .filter_by(user_id=user_id)
        .order_by(CalendarFeed.name)
        .all()
    )


def create_feed(user_id: int, job_id: int, name: str, url: str) -> CalendarFeed:
    feed = CalendarFeed(user_id=user_id, job_id=job_id, name=name, url=url)
    db.session.add(feed)
    db.session.commit()
    return feed


def delete_feed(feed: CalendarFeed) -> None:
    db.session.delete(feed)
    db.session.commit()


def get_feed_or_404(feed_id: int, user_id: int) -> CalendarFeed:
    return CalendarFeed.query.filter_by(id=feed_id, user_id=user_id).first_or_404()


def sync_feed(feed: CalendarFeed) -> dict:
    """
    Fetch remote ICS URL and import shifts.
    Returns summary dict from import_shifts_from_ics.
    Raises requests.RequestException on network failure.
    """
    response = requests.get(feed.url, timeout=15)
    response.raise_for_status()

    result = import_shifts_from_ics(
        file_bytes=response.content,
        user_id=feed.user_id,
        job_id=feed.job_id
    )

    feed.last_synced_at = datetime.now(timezone.utc)
    db.session.commit()

    return result


def get_active_jobs_for_user(user_id: int):
    return Job.query.filter_by(user_id=user_id, is_active=True).all()