import asyncio

from aiokafka import AIOKafkaConsumer


class ConsumerService:
    def __init__(self, bootstrap_servers, group_id, topic) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topic = topic
        self.consumer = AIOKafkaConsumer(
            self.topic,
            loop=asyncio.get_event_loop(),
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset='earliest'
        )

    async def consume_messages(self):
        await self.consumer.start()
        try:
            while True:
                async for msg in self.consumer:
                    print(f"""
                        Consumed message: key = {msg.key},
                        value = {msg.value},
                        offset = {msg.offset}
                    """)
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            await self.consumer.stop()