import io, base64
from datetime import date
from flask import Blueprint, send_file
from .extensions import db
from .models import EmailTrack, WarmupLog

tracking_bp = Blueprint("tracking", __name__)

_pixel = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAuMBgUjU0LcAAAAASUVORK5CYII="
)

@tracking_bp.route("/track/<uid>.png")
def track(uid):
    et = EmailTrack.query.filter_by(uid=uid).first()
    if et:
        today = date.today()
        log = WarmupLog.query.filter_by(domain_id=et.domain_id, send_date=today).first()
        if not log:
            from .models import WarmupLog
            log = WarmupLog(domain_id=et.domain_id, send_date=today, sent_count=0, open_count=1)
            db.session.add(log)
        else:
            log.open_count += 1
        db.session.commit()
    return send_file(io.BytesIO(_pixel), mimetype="image/png")
