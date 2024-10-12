from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP

from core.config import settings
from type import MessageType, Message
from services.abstract_observer import AbstractMessageObserver

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

    async def send(
        self, recipient: str, recipient_name: str, message: str, type: MessageType
    ) -> bool:
        """Отправляет форматированное сообщение указанному пользователю"""
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = recipient
        msg['Subject'] = self.message_subject[type]

        html_template = self.render_template(f"{type}.html", name=recipient_name, link=message)

        msg.attach(MIMEText(html_template, 'html'))
        try:
            async with SMTP(hostname=self.smtp_host, port=self.smtp_port, timeout=10) as server:
                await server.login(self.smtp_user, self.smtp_password)
                await server.sendmail(self.smtp_user, recipient, msg.as_string())
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def render_template(self, template_name: str, **params) -> str:
        """Загрузка и предварительная настройка html шаблона"""
        template_path = settings.TEMPLATES_DIR / template_name

        with open(template_path, 'r', encoding='utf-8') as file:
            template = file.read()

        for key, value in params.items():
            template = template.replace(f'{{{key}}}', str(value))

        return template


class EmailMessageObserver(AbstractMessageObserver, EmailService):
    def __init__(
        self, smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str
    ) -> None:
        super().__init__(smtp_host, smtp_port, smtp_user, smtp_password)

    async def send_message(self, message: Message):
        await self.send(
            recipient=message.recipient,
            recipient_name=message.recipient_name,
            message=message.message,
            type=message.message_type
        )