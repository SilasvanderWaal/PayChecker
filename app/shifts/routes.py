from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.shifts import shifts_bp
from app.shifts.forms import ShiftForm, ICSImportForm
from app.shifts.services import(
    get_user_shifts, create_shift, update_shift,
    delete_shift, get_shift_or_404, get_active_jobs_for_user,
    import_shifts_from_ics
)

def populate_job_choices(form, user_id):
    """Populate the job dropdown with the users active jobs"""
    jobs = get_active_jobs_for_user(user_id)
    form.job_id.choices = [(job.id, job.name) for job in jobs]
    return jobs

@shifts_bp.route("/")
@login_required
def index():
    shifts = get_user_shifts(current_user.id)
    return render_template("shifts/index.html", shifts=shifts)

@shifts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = ShiftForm()
    populate_job_choices(form, current_user.id)
    if form.validate_on_submit():
        create_shift(
            user_id=current_user.id,
            job_id=form.job_id.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            break_duration=form.break_duration.data,
            notes=form.notes.data
        )
        flash("Shift added.", "success")
        return redirect(url_for("shifts.index"))
    return render_template("shifts/form.html", form=form, title="Add Shift")

@shifts_bp.route("/<int:shift_id>/edit", methods=["GET", "POST"])
@login_required
def edit(shift_id):
    shift = get_shift_or_404(shift_id, current_user.id)
    form = ShiftForm(obj=shift)
    populate_job_choices(form, current_user.id)
    if form.validate_on_submit():
        update_shift(
            shift=shift,
            job_id=form.job_id.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            break_duration=form.break_duration.data,
            notes=form.notes.data
        )
        flash("Shift updated.", "success")
        return redirect(url_for("shifts.index"))
    return render_template("shifts/form.html", form=form, title="Edit Shift")


@shifts_bp.route("/<int:shift_id>/delete", methods=["POST"])
@login_required
def delete(shift_id):
    shift = get_shift_or_404(shift_id, current_user.id)
    delete_shift(shift)
    flash("Shift deleted.", "success")
    return redirect(url_for("shifts.index"))

@shifts_bp.route("/import", methods=["GET", "POST"])
@login_required
def ics_import():
    form = ICSImportForm()
    populate_job_choices(form, current_user.id)
    if form.validate_on_submit():
        file_bytes = form.ics_file.data.read()
        result = import_shifts_from_ics(
            file_bytes=file_bytes,
            user_id=current_user.id,
            job_id=form.job_id.data
        )
        flash(
            f"Import complete: {result['created']} created, {result['updated']} updated.",
            "success"
        )
        return redirect(url_for("shifts.index"))
    return render_template("shifts/ics_import.html", form=form)