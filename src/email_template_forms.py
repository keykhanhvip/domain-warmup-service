from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class TemplateForm(FlaskForm):
    name         = StringField("Template Name", validators=[DataRequired()])
    subject      = StringField("Subject", validators=[DataRequired()])
    html_content = TextAreaField("HTML Content", validators=[DataRequired()])
    text_content = TextAreaField("Text Content", validators=[DataRequired()])
    submit       = SubmitField("Save")
