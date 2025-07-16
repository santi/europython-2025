import logging
import asyncio
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config
from contextlib import asynccontextmanager
from testcontainers.kafka import KafkaContainer

from user_api.services.user_service import UserService
from user_api.models.users import UserCreate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    kafka = KafkaContainer("confluentinc/cp-kafka:7.6.0")
    kafka.start()

    loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=kafka.get_bootstrap_server()
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await producer.start()
        yield
        await producer.stop()
        kafka.stop()

    user_service = UserService(producer=producer)

    app = FastAPI(lifespan=lifespan, title="Core API", version="1.0.0")

    @app.post("/users")
    async def create_user(user: UserCreate):
        """Create a new user"""
        await user_service.create_user(user)
        return {"status": "OK"}

    @app.get("/users")
    async def dummy_user():
        """Create a new user"""
        await user_service.create_user(UserCreate(name="testuser", email="sdfsd"))
        return {"status": "OK"}

    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return {"message": "User API is running!", "status": "healthy"}

    config = Config()
    config.bind = ["localhost:8081"]

    asyncio.run(serve(app, config), loop_factory=lambda: asyncio.get_event_loop())


if __name__ == "__main__":
    main()
