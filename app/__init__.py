from flask import Flask
from app.extensions import db, login_manager, csrf, bcrypt, migrate
from app.config import config_by_name
import app.models

import os


def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_name[env])

    # Initialise extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.jobs import jobs_bp
    app.register_blueprint(jobs_bp)

    from app.shifts import shifts_bp
    app.register_blueprint(shifts_bp)

    from app.calendar_feeds import calendar_feeds_bp
    app.register_blueprint(calendar_feeds_bp)

    from flask import render_template

    @app.route("/")
    def dashboard():
        return "Dashboard coming up!"

    return app