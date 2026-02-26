from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.jobs import jobs_bp
from app.jobs.forms import JobForm
from app.jobs.services import get_user_jobs, create_job, update_job, get_job_or_404


@jobs_bp.route("/")
@login_required
def index():
    jobs = get_user_jobs(current_user.id)
    return render_template("jobs/index.html", jobs=jobs)


@jobs_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = JobForm()
    if form.validate_on_submit():
        create_job(
            user_id=current_user.id,
            name=form.name.data,
            hourly_rate=form.hourly_rate.data,
            currency=form.currency.data
        )
        flash("Job created.", "success")
        return redirect(url_for("jobs.index"))
    return render_template("jobs/form.html", form=form, title="Add Job")


@jobs_bp.route("/<int:job_id>/edit", methods=["GET", "POST"])
@login_required
def edit(job_id):
    job = get_job_or_404(job_id, current_user.id)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        update_job(
            job=job,
            name=form.name.data,
            hourly_rate=form.hourly_rate.data,
            currency=form.currency.data,
            is_active=form.is_active.data
        )
        flash("Job updated.", "success")
        return redirect(url_for("jobs.index"))
    return render_template("jobs/form.html", form=form, title="Edit Job")