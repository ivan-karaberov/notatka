import json
import asyncio
import logging

from aiokafka import AIOKafkaProducer

from core.config import settings
from schemas.account import ConfirmationCodeMessageSchema

log = logging.getLogger(__name__)


class ProducerService:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            loop=asyncio.get_running_loop(),
            bootstrap_servers=self.bootstrap_servers
        )
        try:
            await self.producer.start()
        except Exception as e:
            log.error("Producer Service not started: %s", e)

    async def stop(self):
        await self.producer.stop()
        self.producer = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
    
    async def send(self, topic, key, value):
        try:
            await self.producer.send_and_wait(
                topic=topic,
                value=value.encode('utf-8'),
                key=key.encode('utf-8')
            )
        except Exception as e:
            log.error("Message not send to ProducerService: %s", e)


class NotificationService(ProducerService):
    def __init__(self) -> None:
        self.topic = 'account-topic'
        super().__init__(settings.broker.get_url())

    async def send_message(self, message: ConfirmationCodeMessageSchema) -> None:
        try:
            message = json.dumps(message.__dict__)
            await self.send(self.topic, "email", message)
        except Exception as e:
            logging.error("Error sending message: %s", e)