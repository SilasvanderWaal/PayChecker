import requests
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.calendar_feeds import calendar_feeds_bp
from app.calendar_feeds.forms import CalendarFeedForm
from app.calendar_feeds.services import (
    get_user_feeds, create_feed, delete_feed,
    get_feed_or_404, sync_feed, get_active_jobs_for_user
)


def populate_job_choices(form, user_id):
    jobs = get_active_jobs_for_user(user_id)
    form.job_id.choices = [(job.id, job.name) for job in jobs]


@calendar_feeds_bp.route("/")
@login_required
def index():
    feeds = get_user_feeds(current_user.id)
    return render_template("calendar_feeds/index.html", feeds=feeds)


@calendar_feeds_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = CalendarFeedForm()
    populate_job_choices(form, current_user.id)
    if form.validate_on_submit():
        create_feed(
            user_id=current_user.id,
            job_id=form.job_id.data,
            name=form.name.data,
            url=form.url.data
        )
        flash("Calendar feed added.", "success")
        return redirect(url_for("calendar_feeds.index"))
    return render_template("calendar_feeds/form.html", form=form, title="Add Calendar Feed")


@calendar_feeds_bp.route("/<int:feed_id>/sync", methods=["POST"])
@login_required
def sync(feed_id):
    feed = get_feed_or_404(feed_id, current_user.id)
    try:
        result = sync_feed(feed)
        flash(
            f"Sync complete: {result['created']} created, {result['updated']} updated.",
            "success"
        )
    except requests.RequestException as e:
        flash(f"Sync failed: {str(e)}", "danger")
    return redirect(url_for("calendar_feeds.index"))


@calendar_feeds_bp.route("/<int:feed_id>/delete", methods=["POST"])
@login_required
def delete(feed_id):
    feed = get_feed_or_404(feed_id, current_user.id)
    delete_feed(feed)
    flash("Calendar feed deleted.", "success")
    return redirect(url_for("calendar_feeds.index"))