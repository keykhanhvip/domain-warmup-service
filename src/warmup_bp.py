
from flask import Blueprint, render_template
from flask_login import login_required

warmup_bp = Blueprint('warmup', __name__)

@warmup_bp.route('/warmup/schedule')
@login_required
def schedule():
    return render_template('warmup_schedule.html')
