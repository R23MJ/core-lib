"""Defines the ProjectRepo interface for managing project repositories."""
from abc import ABC, abstractmethod
from core_lib.domain import Project, ProjectCreateArgs, ProjectUpdateArgs

class ProjectRepository(ABC):
    """
    Abstract base class for project repository management.
    This class defines the interface for managing project repositories
    and provides methods for creating, deleting, and checking the status of repositories.
    """

    @abstractmethod
    async def get(self, user_id: str, project_id: str) -> Project | None:
        """
        Retrieve a project repository by its ID.
        :param project_id: The ID of the project repository to retrieve.
        :return: The project repository object.
        """

    @abstractmethod
    async def get_all(self, user_id: str) -> list[Project]:
        """
        Retrieve all project repositories for a user.
        :param user_id: The ID of the user whose project repositories to retrieve.
        :return: A list of project repository objects.
        """

    @abstractmethod
    async def create(self, user_id: str, project_create_args: ProjectCreateArgs) -> Project | None:
        """
        Create a new project repository.
        :param user_id: The ID of the user creating the project repository.
        :param project: The project repository object to create.
        :return: The created project repository object.
        """

    @abstractmethod
    async def update(self, user_id: str, project_id: str, project_update_args: ProjectUpdateArgs) -> bool:
        """
        Update an existing project repository.
        :param user_id: The ID of the user updating the project repository.
        :param project_id: The ID of the project repository to update.
        :param project: The updated project repository object.
        :return: The updated project repository object.
        """

    @abstractmethod
    async def delete(self, user_id: str, project_id: str) -> bool:
        """
        Delete a project repository by its ID.
        :param user_id: The ID of the user deleting the project repository.
        :param project_id: The ID of the project repository to delete.
        :return: The deleted project repository object.
        """
