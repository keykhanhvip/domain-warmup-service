import smtplib
from email.mime.text import MIMEText
from datetime import date
from .extensions import db
from .models import Domain, WarmupLog
from .models import EmailTrack, EmailTemplate
from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask import url_for
import uuid

class WarmupEngine:
    def run(self):
        today = date.today()
        domains = Domain.query.filter_by(status="warming").all()
        for dom in domains:
            sent = self._send(dom)
            metrics = self._fetch(dom)
            metrics['sent_count'] = sent
            log = WarmupLog.query.filter_by(domain_id=dom.id, send_date=today).first()
            if not log:
                log = WarmupLog(domain_id=dom.id, send_date=today, **metrics)
                db.session.add(log)
            else:
                for k, v in metrics.items():
                    setattr(log, k, getattr(log, k) + v)
            db.session.commit()

    def _send(self, dom, count=5):
        sent = 0
        with smtplib.SMTP(dom.smtp_host, dom.smtp_port) as s:
            s.starttls()
            s.login(dom.smtp_user, dom.smtp_pass)
            for i in range(count):
                msg = MIMEText(f"Warm-up ping #{i+1}")
                msg["Subject"] = f"Warm-Up #{i+1}"
                msg["From"] = dom.smtp_user
                msg["To"] = dom.smtp_user
                try:
                    s.sendmail(dom.smtp_user, [dom.smtp_user], msg.as_string())
                    sent += 1
                except:
                    pass
        return sent

    def _fetch(self, dom):
        # TODO: implement IMAP parsing or webhook logic
        return {
            "open_count": 0,
            "bounce_count": 0,
            "unsub_count": 0,
            "complaint_count": 0
        }



    def send_one(self, dom, subject, body):
        import smtplib
        from email.mime.text import MIMEText

        sent = 0
        try:
            with smtplib.SMTP(dom.smtp_host, dom.smtp_port) as s:
                s.starttls()
                s.login(dom.smtp_user, dom.smtp_pass)
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = dom.smtp_user
                msg["To"] = dom.smtp_user
                s.sendmail(dom.smtp_user, [dom.smtp_user], msg.as_string())
                sent = 1
        except Exception as e:
            print("Error sending test email:", e)
        return sent


    def send_template(self, dom, template_id, context: dict):
        tmpl = EmailTemplate.query.get_or_404(template_id)
        html = jinja_env.from_string(tmpl.html_content).render(**context)
        text = jinja_env.from_string(tmpl.text_content).render(**context)
        uid = str(uuid.uuid4())
        et = EmailTrack(uid=uid, domain_id=dom.id, template_id=tmpl.id)
        db.session.add(et)
        db.session.flush()
        track_url = url_for("tracking.track", uid=uid, _external=True)
        html += f'<img src="{track_url}" width="1" height="1" alt="" />'
        msg = MIMEMultipart('alternative')
        msg['Subject'] = tmpl.subject
        msg['From']    = dom.smtp_user
        msg['To']      = dom.smtp_user
        part1 = MIMEText(text, 'plain', 'utf-8')
        part2 = MIMEText(html, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)
        try:
            with smtplib.SMTP(dom.smtp_host, dom.smtp_port) as s:
                s.starttls()
                s.login(dom.smtp_user, dom.smtp_pass)
                s.sendmail(dom.smtp_user, [dom.smtp_user], msg.as_string())
            db.session.commit()
            return 1
        except Exception as e:
            db.session.rollback()
            print("Error send_template:", e)
            return 0
