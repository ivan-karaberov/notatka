from services.EmailService import EmailService
from core.config import settings
from enums import EmailType

es = EmailService(
    smtp_host=settings.smtp.SMTP_HOST,
    smtp_port=settings.smtp.SMTP_PORT,
    smtp_user=settings.smtp.SMTP_USER,
    smtp_password=settings.smtp.SMTP_PASSWORD
)

es.send_message("Ivan", "https://github.com/ivan-karaberov", EmailType.confirmation_email, "karaberovivan5@gmail.com")