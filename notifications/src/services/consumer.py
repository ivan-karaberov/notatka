import json

from aiokafka import AIOKafkaConsumer

from services.abstract_observer import *


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
            print(f"Error occurred: {e}")
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
        await self.consumer.start()

    async def process_message(self, msg) -> None:
        print(msg)


class BrokerMessagePublisher(AbstractMessagePublisher, ConsumerService):
    def __init__(self, bootstrap_servers, group_id, topic) -> None:
        self.__observers = {}
        super().__init__(bootstrap_servers, group_id, topic)

    def attach(self, observer_id: str, observer: AbstractMessageObserver) -> None:
        self.__observers[observer_id] = observer

    def detach(self, observer_id: str) -> None:
        self.__observers.pop(observer_id, None)

    async def process_message(self, msg) -> None:
        value = json.loads(msg.value)

        channel = msg.key.decode("utf-8")
        message = Message(
            recipient=value.get("recipient"),
            recipient_name=value.get("recipient_name"),
            message=value.get("message"),
            message_type=value.get("message_type")
        )
        print(channel, message)
        await self.notify(channel, message)

    async def notify(self, observer_id: str, message: Message) -> None:
        if observer := self.__observers.get(observer_id):
            await observer.send_message(message)
