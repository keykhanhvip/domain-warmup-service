from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .extensions import db
from .models import Domain
from .domain_forms import DomainForm
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# request
from .warmup_engine import WarmupEngine
from .models import EmailTemplate
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# request


domains_bp = Blueprint("domains", __name__, template_folder="templates")

@domains_bp.route("/", methods=["GET","POST"])
@login_required
def list_add():
    form = DomainForm()
    if form.validate_on_submit():
        dom = Domain(
            user_id=current_user.id,
            name=form.name.data,
            smtp_host=form.smtp_host.data, smtp_port=form.smtp_port.data,
            smtp_user=form.smtp_user.data, smtp_pass=form.smtp_pass.data,
            imap_host=form.imap_host.data, imap_port=form.imap_port.data,
            imap_user=form.imap_user.data, imap_pass=form.imap_pass.data
        )
        db.session.add(dom); db.session.commit()
        flash("Thêm domain thành công")
        return redirect(url_for("domains.list_add"))
    domains = Domain.query.filter_by(user_id=current_user.id).all()
    return render_template("domains.html", form=form, domains=domains)

@domains_bp.route("/<int:did>/delete")
@login_required
def delete(did):
    dom = Domain.query.get_or_404(did)
    if dom.user_id == current_user.id:
        db.session.delete(dom); db.session.commit()
        flash("Đã xóa domain")
    else:
        flash("Không có quyền")
    return redirect(url_for("domains.list_add"))


@domains_bp.route("/<int:did>/send_test", methods=["POST"])
@login_required
def send_test(did):
    dom = Domain.query.get_or_404(did)
    if dom.user_id != current_user.id:
        flash("Bạn không có quyền gửi thư với domain này", "error")
        return redirect(url_for("domains.list_add"))
    subject = request.form.get("subject", "Test Email")
    body = request.form.get("body", "Hello from Warm-Up Service")
    engine = WarmupEngine()
    sent = engine.send_one(dom, subject, body)
    flash(f"Đã gửi {sent} thư thử nghiệm đến {{dom.smtp_user}}", "success")
    return redirect(url_for("domains.list_add"))

@domains_bp.route("/<int:did>/send_template", methods=["POST"])
@login_required
def send_template_route(did):
    dom = Domain.query.get_or_404(did)
    if dom.user_id != current_user.id:
        flash("Không có quyền", "danger")
        return redirect(url_for("domains.list_add"))
    template_id = int(request.form.get("template_id"))
    context = {"name": current_user.email}
    sent = WarmupEngine().send_template(dom, template_id, context)
    flash(f"Đã gửi {sent} thư theo template.", "success")
    return redirect(url_for("domains.list_add"))
