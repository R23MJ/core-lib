"""Defines the UserRepo interface for managing User repositories."""
from abc import ABC, abstractmethod
from core_lib.domain import User, UserCreateArgs, UserUpdateArgs

class UserRepository(ABC):
    """
    Abstract base class for User repository management.
    This class defines the interface for managing User repositories, including
    creating, retrieving, updating, and deleting User repositories.
    """

    @abstractmethod
    async def get(self, user_id: str) -> User | None:
        """
        Retrieve a User by its ID.
        :param user_id: The ID of the User to retrieve.
        :return: The User object.
        """

    @abstractmethod
    async def create(self, user_create_args: UserCreateArgs) -> User | None:
        """
        Create a new User.
        :return: The created User repository object.
        """

    @abstractmethod
    async def update(self, user_id: str, user_update_args: UserUpdateArgs) -> bool:
        """
        Update an existing User.
        :param user_id: The ID of the User to update.
        :param User: The updated User object.
        :return: True on success.
        """

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """
        Delete a User by its ID.
        :param user_id: The ID of the User to delete.
        :return: True on success.
        """
