from flask import render_template
from flask_login import login_required, current_user
from app.dashboard import dashboard_bp
from app.dashboard.services import get_dashboard_data


@dashboard_bp.route("/")
@login_required
def index():
    data = get_dashboard_data(current_user.id)
    return render_template("dashboard/index.html", **data)