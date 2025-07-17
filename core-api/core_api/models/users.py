from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from psycopg.rows import dict_row

from core_api.db.pool import DatabasePool


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Repository implementation
class UserRepository:
    def __init__(self, db_pool: DatabasePool):
        self.db_pool = db_pool

    async def initialize(self):
        """Initialize the repository, e.g., create tables if needed"""
        async with self.db_pool.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    --sql
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        created_at TIMESTAMP NOT NULL DEFAULT now()
                    );
                    """)
                await conn.commit()

    async def create_user(self, user: UserCreate) -> UserResponse:
        """Create a new user in the database"""
        async with self.db_pool.get_connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cursor:
                await cursor.execute(
                    """
                    INSERT INTO users (name, email)
                    VALUES (%(name)s, %(email)s)
                    RETURNING id, name, email, created_at
                    """,
                    {"name": user.name, "email": user.email},
                )
                row = await cursor.fetchone()
                return UserResponse(**row)

    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Get user by ID"""
        async with self.db_pool.get_connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cursor:
                await cursor.execute(
                    "SELECT id, name, email, created_at FROM users WHERE id = %s",
                    (user_id,),
                )
                row = await cursor.fetchone()
                return UserResponse(**row) if row else None

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        """Get all users with pagination"""
        async with self.db_pool.get_connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cursor:
                await cursor.execute(
                    "SELECT id, name, email, created_at FROM users ORDER BY id OFFSET %s LIMIT %s",
                    (skip, limit),
                )
                rows = await cursor.fetchall()
                return [UserResponse(**row) for row in rows]

    async def delete_users(self):
        """Delete all users"""
        async with self.db_pool.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM users")
                await conn.commit()