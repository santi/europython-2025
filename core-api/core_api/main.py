import json
import logging
import asyncio
from time import sleep
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config
from contextlib import asynccontextmanager
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer

from core_api.db.pool import DatabasePool
from core_api.services.user_service import UserService
from core_api.models.users import UserCreate, UserResponse, UserRepository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    postgres = PostgresContainer("postgres:17")
    postgres.start()
    kafka = KafkaContainer("confluentinc/cp-kafka:7.6.0").with_bind_ports(9093, 9093)
    kafka.start()

    connection_string = f"postgresql://{postgres.username}:{postgres.password}@{postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}/{postgres.dbname}"
    db_pool = DatabasePool(connection_string=connection_string)
    user_repository = UserRepository(db_pool=db_pool)
    user_service = UserService(user_repository=user_repository)
    
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer("users",
        loop=loop, bootstrap_servers=kafka.get_bootstrap_server(), group_id="test"
    )

    
    async def consume_messages():
        async for msg in consumer:
            print(f"Consumed message: {msg.value.decode('utf-8')}")
            user_create = UserCreate.model_validate(json.loads(msg.value.decode('utf-8')))
            await user_service.create_user(
                user_create
            )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            await db_pool.initialize()
            await user_repository.initialize()
            await consumer.start()
            await asyncio.sleep(2)  # Allow some time for the consumer to start
            asyncio.create_task(consume_messages())
            yield
            await consumer.stop()
            await db_pool.close()
        finally:
            kafka.stop()
            postgres.stop()


    app = FastAPI(lifespan=lifespan, title="Core API", version="1.0.0")

    @app.get("/users", response_model=list[UserResponse])
    async def get_users(
        skip: int = 0,
        limit: int = 100,
    ):
        """Fetch all users with pagination"""
        return await user_service.get_users(skip, limit)

    @app.get("/users/{user_id}", response_model=UserResponse)
    async def get_user(user_id: int):
        """Fetch a specific user by ID"""
        return await user_service.get_user_by_id(user_id)

    @app.post("/users", response_model=UserResponse)
    async def create_user(user: UserCreate):
        """Create a new user"""
        return await user_service.create_user(user)
    
    @app.delete("/users")
    async def delete_users():
        await user_service.delete_users()
        return {"status": "Users deleted successfully"}

    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return {"message": "Core API is running!", "status": "healthy"}

    config = Config()
    config.bind = ["localhost:8080"]

    asyncio.run(serve(app, config), loop_factory=lambda: asyncio.get_event_loop())


if __name__ == "__main__":
    main()
