from core_lib.domain import Project, ProjectCreateArgs, ProjectUpdateArgs
from . import ProjectRepository

class NoopProjectRepository(ProjectRepository):
    """No-op implementation of the ProjectRepository interface."""

    def __init__(self):
        pass

    async def get(self, user_id: str, project_id: str) -> Project | None:
        """Retrieve a project repository by its ID."""
        return Project(
            id=project_id,
            repo_url="test_repo_url",
            env={"test_env": "test_value"},
            status="testing",
        )

    async def get_all(self, user_id: str) -> list[Project]:
        """Retrieve all project repositories for a user."""
        return [
            Project(
                id="1",
                repo_url="test_repo_url_1",
                env={"test_env": "test_value_1"},
                status="testing",
            ),
            Project(
                id="2",
                repo_url="test_repo_url_2",
                env={"test_env": "test_value_2"},
                status="testing",
            ),
        ]

    async def create(self, user_id: str, project_create_args: ProjectCreateArgs) -> Project | None:
        """Create a new project repository."""
        new_project = Project(
            id="1",
            repo_url=project_create_args.repo_url,
            env=project_create_args.env,
            status="testing",
        )

        return new_project

    async def update(self, user_id: str, project_id: str, project_update_args: ProjectUpdateArgs) -> bool:
        """Update an existing project repository."""
        return True

    async def delete(self, user_id: str, project_id: str) -> bool:
        """Delete a project repository by its ID."""
        return True
