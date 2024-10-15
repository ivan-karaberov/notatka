import asyncio
import logging

from core.config import settings
from services.consumer import BrokerMessagePublisher
from services.email import EmailMessageObserver
from utils.logging_config import configure_logging


log = logging.getLogger(__name__)


async def main():
    configure_logging()

    broker_publisher = BrokerMessagePublisher(
        bootstrap_servers=settings.broker.get_url(),
        group_id='account-group',
        topic='account-topic'
    )

    email_observer = EmailMessageObserver(
        smtp_host=settings.smtp.SMTP_HOST,
        smtp_port=settings.smtp.SMTP_PORT,
        smtp_user=settings.smtp.SMTP_USER,
        smtp_password=settings.smtp.SMTP_PASSWORD
    )

    broker_publisher.attach("email", email_observer)

    try:
        await broker_publisher.consume_messages()
    except Exception as e:
        log.error("Error in consume_message > %s", e)


if __name__ == '__main__':
    asyncio.run(main())