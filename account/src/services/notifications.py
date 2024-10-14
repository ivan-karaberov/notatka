import json
import asyncio

from aiokafka import AIOKafkaProducer

from core.config import settings
from schemas.account import ConfirmationCodeMessageSchema


class ProducerService:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            loop=asyncio.get_running_loop(),
            bootstrap_servers=self.bootstrap_servers
        )
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()
        self.producer = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
    
    async def send(self, topic, key, value):
        await self.producer.send_and_wait(
            topic=topic,
            value=value.encode('utf-8'),
            key=key.encode('utf-8')
        )


class NotificationService(ProducerService):
    def __init__(self) -> None:
        self.topic = 'account-topic'
        super().__init__(settings.broker.get_url())

    async def send_message(self, message: ConfirmationCodeMessageSchema) -> None:
        print(message.__dict__)
        message = json.dumps(message.__dict__)
        await self.send(self.topic, "email", message)