from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role     = db.Column(db.String(20), default='client')
    daily_quota = db.Column(db.Integer, default=200)
    emails_sent_today = db.Column(db.Integer, default=0)
    last_sent_at = db.Column(db.DateTime)
    domains  = db.relationship("Domain", backref="owner", lazy=True)

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)
    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

class Domain(db.Model):
    __tablename__ = "domains"
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name        = db.Column(db.String(255), nullable=False)
    smtp_host   = db.Column(db.String(255)); smtp_port = db.Column(db.Integer)
    smtp_user   = db.Column(db.String(255)); smtp_pass = db.Column(db.String(255))
    imap_host   = db.Column(db.String(255)); imap_port = db.Column(db.Integer)
    imap_user   = db.Column(db.String(255)); imap_pass = db.Column(db.String(255))
    status      = db.Column(db.String(20), default="idle", nullable=False)
    created_at  = db.Column(db.DateTime, server_default=db.func.now())
    logs        = db.relationship("WarmupLog", backref="domain", lazy=True)

class WarmupLog(db.Model):
    __tablename__ = "warmup_logs"
    id              = db.Column(db.Integer, primary_key=True)
    domain_id       = db.Column(db.Integer, db.ForeignKey("domains.id"), nullable=False)
    send_date       = db.Column(db.Date, default=date.today, nullable=False)
    sent_count      = db.Column(db.Integer, default=0)
    open_count      = db.Column(db.Integer, default=0)
    bounce_count    = db.Column(db.Integer, default=0)
    unsub_count     = db.Column(db.Integer, default=0)
    complaint_count = db.Column(db.Integer, default=0)

    __table_args__ = (
        db.UniqueConstraint("domain_id", "send_date", name="uq_domain_date"),
    )

class EmailTemplate(db.Model):
    __tablename__ = "email_templates"
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), unique=True, nullable=False)
    subject      = db.Column(db.String(255), nullable=False)
    html_content = db.Column(db.Text, nullable=False)
    text_content = db.Column(db.Text, nullable=False)
    created_at   = db.Column(db.DateTime, server_default=db.func.now())

class EmailTrack(db.Model):
    __tablename__ = "email_tracks"
    id          = db.Column(db.Integer, primary_key=True)
    uid         = db.Column(db.String(36), unique=True, nullable=False)
    domain_id   = db.Column(db.Integer, db.ForeignKey("domains.id"), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey("email_templates.id"), nullable=False)
    created_at  = db.Column(db.DateTime, server_default=db.func.now())

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
