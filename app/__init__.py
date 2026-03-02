from flask import Flask
from app.extensions import db, login_manager, csrf, bcrypt, migrate
from app.config import config_by_name

import os


def create_app():
    flask_app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    flask_app.config.from_object(config_by_name[env])

    db.init_app(flask_app)
    login_manager.init_app(flask_app)
    csrf.init_app(flask_app)
    bcrypt.init_app(flask_app)
    migrate.init_app(flask_app, db)

    import app.models  # noqa: F401

    from app.auth import auth_bp
    flask_app.register_blueprint(auth_bp)

    from app.jobs import jobs_bp
    flask_app.register_blueprint(jobs_bp)

    from app.shifts import shifts_bp
    flask_app.register_blueprint(shifts_bp)

    from app.calendar_feeds import calendar_feeds_bp
    flask_app.register_blueprint(calendar_feeds_bp)

    from app.payslips import payslips_bp
    flask_app.register_blueprint(payslips_bp)

    from app.ob_rules import ob_rules_bp
    flask_app.register_blueprint(ob_rules_bp)

    from app.dashboard import dashboard_bp
    flask_app.register_blueprint(dashboard_bp)

    from app.scheduler import init_scheduler
    import logging
    logging.basicConfig(level=logging.INFO)
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        init_scheduler(flask_app)

    return flask_app