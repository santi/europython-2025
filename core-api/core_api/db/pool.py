import logging
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


# Database connection pool
class DatabasePool:
    def __init__(self, connection_string: str):
        self.pool = AsyncConnectionPool(
            open=False,
            conninfo=connection_string,
            min_size=1,
            max_size=20,
            timeout=30,
        )

    async def initialize(self):
        """Initialize the connection pool"""
        try:
            await self.pool.open()
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise e

    async def close(self):
        """Close the connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

    @asynccontextmanager
    async def get_connection(self):
        """Get a connection from the pool"""
        async with self.pool.connection() as conn:
            yield conn
