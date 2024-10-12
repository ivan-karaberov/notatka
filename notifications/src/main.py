import asyncio

from core.config import settings
from services.consumer import BrokerMessagePublisher
from services.email import EmailMessageObserver

async def main():
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
    except KeyboardInterrupt:
        print("Consumer stopped.")
    except Exception as e:
        print(f"Error > {e}")


if __name__ == '__main__':
    asyncio.run(main())