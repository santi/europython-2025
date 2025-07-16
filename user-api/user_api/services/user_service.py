from aiokafka import AIOKafkaProducer

from user_api.models.users import UserCreate


class UserService:
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def create_user(self, user: UserCreate) -> None:
        """Create a new user with business logic validation"""
        await self.producer.send_and_wait(
            topic="users",
            key="#".encode("utf-8"),
            value=user.model_dump_json().encode("utf-8"),
        )
