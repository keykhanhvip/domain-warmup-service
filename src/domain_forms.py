from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class DomainForm(FlaskForm):
    name = StringField('Domain Name', validators=[DataRequired()])
    smtp_host = StringField('SMTP Host', validators=[DataRequired()])
    smtp_port = IntegerField('SMTP Port', validators=[DataRequired()])
    smtp_user = StringField('SMTP User', validators=[DataRequired()])
    smtp_pass = PasswordField('SMTP Password')
    imap_host = StringField('IMAP Host')
    imap_port = IntegerField('IMAP Port')
    imap_user = StringField('IMAP User')
    imap_pass = PasswordField('IMAP Password')
    submit = SubmitField('Add Domain')
