from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.ob_rules import ob_rules_bp
from app.ob_rules.forms import OBRuleForm
from app.ob_rules.services import (
    get_rules_for_job, create_rule, delete_rule,
    get_rule_or_404, get_job_or_404_scoped
)


@ob_rules_bp.route("/")
@login_required
def index(job_id):
    job = get_job_or_404_scoped(job_id, current_user.id)
    rules = get_rules_for_job(job_id)
    return render_template("ob_rules/index.html", job=job, rules=rules)


@ob_rules_bp.route("/create", methods=["GET", "POST"])
@login_required
def create(job_id):
    job = get_job_or_404_scoped(job_id, current_user.id)
    form = OBRuleForm()
    if form.validate_on_submit():
        create_rule(
            job_id=job_id,
            period=form.period.data,
            start_hour=form.start_hour.data,
            start_minute=form.start_minute.data,
            end_hour=form.end_hour.data,
            end_minute=form.end_minute.data,
            percentage=float(form.percentage.data)
        )
        flash("OB rule added.", "success")
        return redirect(url_for("ob_rules.index", job_id=job_id))
    return render_template("ob_rules/form.html", form=form, job=job, title="Add OB Rule")


@ob_rules_bp.route("/<int:rule_id>/delete", methods=["POST"])
@login_required
def delete(job_id, rule_id):
    job = get_job_or_404_scoped(job_id, current_user.id)
    rule = get_rule_or_404(rule_id, job_id)
    delete_rule(rule)
    flash("OB rule deleted.", "success")
    return redirect(url_for("ob_rules.index", job_id=job_id))