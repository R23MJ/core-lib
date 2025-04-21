"""Defines the UserRepo interface for managing User repositories."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core_lib.orm import UserORM
from core_lib.domain import User, UserCreateArgs, UserUpdateArgs
from . import UserRepository

class SQLAlchemyUserRepository(UserRepository):
    """
    Abstract base class for User repository management.
    This class defines the interface for managing User repositories, including
    creating, retrieving, updating, and deleting User repositories.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def _get_orm(self, user_id: str) -> UserORM | None:
        """Retrieve a project repository by its ID."""

        try:
            result = await self.db_session.execute(
                select(UserORM).filter_by(id=user_id)
            )

            return result.scalars().first()
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def get(self, user_id: str) -> User | None:
        """Retrieve a User by its ID."""
        user_orm = await self._get_orm(user_id)

        if user_orm:
            return User.model_validate(user_orm, from_attributes=True)

        return None

    async def create(self, user_create_args: UserCreateArgs) -> User | None:
        """Create a new User."""
        user = UserORM(
            username=user_create_args.username,
            email=user_create_args.email,

            oauth_provider=user_create_args.oauth_provider,
            encrypted_oauth_token=user_create_args.encrypted_oauth_token,
            encrypted_refresh_token=user_create_args.encrypted_refresh_token,
            oauth_token_expires_at=user_create_args.oauth_token_expires_at,
        )

        try:
            self.db_session.add(user)
            await self.db_session.commit()
            await self.db_session.refresh(user)

            return User.model_validate(user, from_attributes=True)
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def update(self, user_id: str, user_update_args: UserUpdateArgs) -> bool:
        """Update an existing User."""
        user_orm = await self._get_orm(user_id)

        if not user_orm:
            return False

        for key, value in user_update_args.model_dump(mode="json", exclude_unset=True).items():
            setattr(user_orm, key, value)

        try:
            await self.db_session.commit()
            await self.db_session.refresh(user_orm)
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def delete(self, user_id: str) -> bool:
        """Delete a User by its ID."""
        user_orm = await self._get_orm(user_id)

        if not user_orm:
            return False

        try:
            await self.db_session.delete(user_orm)
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise e
