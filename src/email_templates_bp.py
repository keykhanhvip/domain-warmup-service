from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from .extensions import db
from .models import EmailTemplate
from .email_template_forms import TemplateForm

template_bp = Blueprint("templates", __name__, template_folder="templates")

@template_bp.route("/templates", methods=["GET"])
@login_required
def list_templates():
    temps = EmailTemplate.query.all()
    return render_template("templates/list.html", templates=temps)

@template_bp.route("/templates/add", methods=["GET","POST"])
@login_required
def add_template():
    form = TemplateForm()
    if form.validate_on_submit():
        t = EmailTemplate(
            name=form.name.data,
            subject=form.subject.data,
            html_content=form.html_content.data,
            text_content=form.text_content.data
        )
        db.session.add(t); db.session.commit()
        flash("Đã thêm template.", "success")
        return redirect(url_for("templates.list_templates"))
    return render_template("templates/form.html", form=form, action="Add")

@template_bp.route("/templates/<int:tid>/edit", methods=["GET","POST"])
@login_required
def edit_template(tid):
    t = EmailTemplate.query.get_or_404(tid)
    form = TemplateForm(obj=t)
    if form.validate_on_submit():
        form.populate_obj(t); db.session.commit()
        flash("Đã cập nhật template.", "success")
        return redirect(url_for("templates.list_templates"))
    return render_template("templates/form.html", form=form, action="Edit")

@template_bp.route("/templates/<int:tid>/delete", methods=["POST"])
@login_required
def delete_template(tid):
    t = EmailTemplate.query.get_or_404(tid)
    db.session.delete(t); db.session.commit()
    flash("Đã xóa template.", "success")
    return redirect(url_for("templates.list_templates"))
