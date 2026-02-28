from datetime import datetime
from flask import render_template
from flask_login import login_required, current_user

from app.payslips import payslips_bp
from app.payslips.forms import PayslipForm
from app.payslips.services import calculate_payslip


@payslips_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = PayslipForm()
    payslip = None
    now = datetime.now()

    # Default to current month
    if not form.is_submitted():
        form.year.data = now.year
        form.month.data = now.month

    if form.validate_on_submit():
        payslip = calculate_payslip(
            user_id=current_user.id,
            year=form.year.data,
            month=form.month.data
        )

    return render_template("payslips/index.html", form=form, payslip=payslip)