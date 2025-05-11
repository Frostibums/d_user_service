import json
import logging

from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

class KafkaEventProducer:
    def __init__(self, bootstrap_servers: str):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    async def start(self):
        await self._producer.start()

    async def stop(self):
        await self._producer.stop()

    async def send_user_created_event(self, user_id: str, email: str, role: str):
        event = {
            "event": "user_created",
            "user_id": user_id,
            "email": email,
            "role": role,
        }
        try:
            await self._producer.send_and_wait("user-events", event)
            logger.info(f"Published user_created for {user_id}")
        except Exception as e:
            logger.error(f"Failed to send Kafka message: {e}")
