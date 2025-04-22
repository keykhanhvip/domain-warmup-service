from flask import Flask, redirect, url_for
from config import Config
from .extensions import db, migrate, login_manager
from .auth import auth_bp
from .warmup_bp import warmup_bp
from .email_templates_bp import template_bp
from .tracking_bp import tracking_bp
from .models import EmailTemplate

from .domains import domains_bp
from .dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(domains_bp, url_prefix="/domains")
    app.register_blueprint(template_bp)
    app.register_blueprint(tracking_bp)
    app.jinja_env.globals['EmailTemplate'] = EmailTemplate
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    @app.route("/")
    def home():
        # redirect to login page by default
        return redirect(url_for("auth.login"))

        app.register_blueprint(warmup_bp)
    return app
