import json
import logging
import asyncio

from aiokafka import AIOKafkaConsumer

from services.abstract_observer import *


log = logging.getLogger(__name__)


class ConsumerService:
    def __init__(self, bootstrap_servers, group_id, topic) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topic = topic
        self.consumer = None

    async def consume_messages(self) -> None:
        """Слушает сообщения в брокере"""
        if self.consumer is None:
            await self.__start_consumer()

        try:
            while True:
                async for msg in self.consumer:
                    await self.process_message(msg)
        except Exception as e:
            log.error("Error when receiving message: %s", e)
        finally:
            await self.consumer.stop()

    async def __start_consumer(self) -> None:
        """Инициализирует слушателя"""
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset='earliest'
        )

        max_retries = 3
        retry_delay = 15  # Задержка между попытками в секундах
        while max_retries > 0:
            try:
                await self.consumer.start()
                break
            except Exception as e:
                log.error("Error start consumer: %s", e)
                max_retries -= 1
                if max_retries:
                    await asyncio.sleep(retry_delay)

    async def process_message(self, msg) -> None:
        print(msg)


class BrokerMessagePublisher(AbstractMessagePublisher, ConsumerService):
    def __init__(self, bootstrap_servers, group_id, topic) -> None:
        self.__observers = {}
        super().__init__(bootstrap_servers, group_id, topic)

    def attach(self, observer_id: str, observer: AbstractMessageObserver) -> None:
        self.__observers[observer_id] = observer
        logging.info("Attached observer: %s", observer_id)

    def detach(self, observer_id: str) -> None:
        self.__observers.pop(observer_id, None)
        logging.info("Detached observer: %s", observer_id)

    async def process_message(self, msg) -> None:
        try:
            value = json.loads(msg.value)

            channel = msg.key.decode("utf-8")
            message = Message(
                recipient=value.get("recipient"),
                recipient_name=value.get("recipient_name"),
                message=value.get("message"),
                message_type=value.get("message_type")
            )

            await self.notify(channel, message)
        except json.JSONDecodeError as e:
            logging.error("JSON decode error: %s for message: %s", e, msg.value)
        except Exception as e:
            logging.error("Error processing message: %s", e)

    async def notify(self, observer_id: str, message: Message) -> None:
        if observer := self.__observers.get(observer_id):
            await observer.send_message(message)
        else:
            log.warning(f"No observer found for id: %s", observer_id)