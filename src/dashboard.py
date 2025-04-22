from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import date
from .extensions import db
from .models import WarmupLog, Domain

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard_bp.route("/")
@login_required
def index():
    today = date.today()
    results = (db.session.query(WarmupLog, Domain.name.label("name"))
               .join(Domain, WarmupLog.domain_id == Domain.id)
               .filter(Domain.owner_id == current_user.id,
                       WarmupLog.send_date == today)
               .all())
    return render_template("dashboard.html", logs=results, date=today)
