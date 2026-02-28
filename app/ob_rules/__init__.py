from flask import Blueprint

ob_rules_bp = Blueprint("ob_rules", __name__, url_prefix="/jobs/<int:job_id>/ob-rules")

from app.ob_rules import routes  # noqa: E402, F401