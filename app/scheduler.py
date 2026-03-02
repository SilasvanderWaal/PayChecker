from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BackgroundScheduler()

def sync_all_feeds():
    """Fetch all active calendar feeds and sync them."""
    from app.extensions import db
    from app.models.calendar_feed import CalendarFeed
    from app.calendar_feeds.services import sync_feed
    import logging

    logger = logging.getLogger(__name__)
    feeds = CalendarFeed.query.all()
    for feed in feeds:
        try:
            result = sync_feed(feed)
            logger.info(
                f"Auto-synced feed {feed.id} ({feed.name}): "
                f"{result['created']} created, {result['updated']} updated"
            )
        except Exception as e:
            logger.error(f"Auto sync failed for feed {feed.id} {feed.name} : {e}")

def init_scheduler(app):
    """Initialise and start the background scheduler with app context"""
    
    def sync_with_context():
        with app.app_context():
            sync_all_feeds()
    
    scheduler.add_job(
        func=sync_with_context,
        trigger=IntervalTrigger(hours=1),
        id="sync_calendar_feeds",
        name="Sync all calendar feeds",
        replace_existing=True    
    )
    scheduler.start()