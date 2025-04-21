"""Noop User Repository for testing purposes."""

import datetime
from core_lib.domain import User, UserCreateArgs, UserUpdateArgs
from . import UserRepository

class NoopUserRepository(UserRepository):
    """A no-operation User repository for testing purposes."""
    def __init__(self):
        pass

    async def get(self, user_id: str) -> User | None:
        """Retrieve a User by its ID."""
        return User(
            id=user_id,
            username="test_user",
            email="test@email.com",
            oauth_provider="test_provider",
            encrypted_oauth_token="encrypted_token",
            encrypted_refresh_token="encrypted_refresh_token",
            oauth_token_expires_at=datetime.datetime.now() + datetime.timedelta(hours=1),
        )

    async def create(self, user_create_args: UserCreateArgs) -> User | None:
        """Create a new User."""
        return User(
                id="42",
                username=user_create_args.username,
                email=user_create_args.email,
                oauth_provider=user_create_args.oauth_provider,
                encrypted_oauth_token="encrypted_token",
                encrypted_refresh_token="encrypted_refresh_token",
                oauth_token_expires_at=datetime.datetime.now() + datetime.timedelta(hours=1),
            )

    async def update(self, user_id: str, user_update_args: UserUpdateArgs) -> bool:
        """Update an existing User."""
        return True

    async def delete(self, user_id: str) -> bool:
        """Delete a User by its ID."""
        return True
