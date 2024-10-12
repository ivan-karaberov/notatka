from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import settings
from enums import EmailType

class EmailService:
    def __init__(
        self, smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str
    ) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.message_subject = {
            "confirmation_email": "Подтверждение email",
            "password_recovery": "Восстановление пароля"
        }

    def send_message(
        self, firstname: str, link: str, type: EmailType, recipient: str
    ) -> bool:
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = recipient
        msg['Subject'] = self.message_subject[type.value]

        html_template = self.render_template(f"{type.value}.html", name=firstname, link=link)

        msg.attach(MIMEText(html_template, 'html'))

        with SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_user, recipient, msg.as_string())

    def render_template(self, template_name: str, **params) -> str:
        template_path = settings.TEMPLATES_DIR / template_name

        with open(template_path, 'r', encoding='utf-8') as file:
            template = file.read()

        for key, value in params.items():
            template = template.replace(f'{{{key}}}', str(value))

        return template