from fastapi import HTTPException


from core_api.models.users import UserRepository, UserCreate, UserResponse


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate) -> UserResponse:
        """Create a new user with business logic validation"""
        return await self.user_repository.create_user(user)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """Get user by ID with error handling"""
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        """Get all users with pagination"""
        if limit > 100:
            limit = 100  # Business rule: max 100 users per request
        return await self.user_repository.get_users(skip, limit)

    async def delete_users(self):
        """Delete all users"""
        await self.user_repository.delete_users()
