"""SQLAlchemyProjectRepo.py
SQLAlchemy implementation of the ProjectRepository interface for managing project repositories."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core_lib.domain import Project, ProjectCreateArgs, ProjectUpdateArgs
from core_lib.orm import ProjectORM
from . import ProjectRepository

class SQLAlchemyProjectRepository(ProjectRepository):
    """
    SQLAlchemy implementation of the ProjectRepository interface for managing project repositories.
    This class provides methods for creating, deleting, and checking the status of repositories
    using SQLAlchemy ORM.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def _get_orm(self, user_id: str, project_id: str) -> ProjectORM | None:
        """Retrieve a project repository by its ID."""

        try:
            result = await self.db_session.execute(
                select(ProjectORM).filter_by(id=project_id, user_id=user_id)
            )

            return result.scalars().first()
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def get(self, user_id: str, project_id: str) -> Project | None:
        """Retrieve a project repository by its ID."""
        project_orm = await self._get_orm(user_id, project_id)

        if project_orm:
            return Project.model_validate(project_orm, from_attributes=True)

        return None

    async def get_all(self, user_id: str) -> list[Project]:
        """Retrieve all project repositories for a user."""

        try:
            result = await self.db_session.execute(
                select(ProjectORM).filter_by(user_id=user_id)
            )

            return [Project.model_validate(project, from_attributes=True) for project in result.scalars().all()]
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def create(self, user_id: str, project_create_args: ProjectCreateArgs) -> Project | None:
        """Create a new project repository."""
        project = ProjectORM(
            repo_url=project_create_args.repo_url,
            environment_variables=project_create_args.environment_variables
        )

        try:
            self.db_session.add(project)
            await self.db_session.commit()
            await self.db_session.refresh(project)
        except Exception as e:
            await self.db_session.rollback()
            raise e

        return await self.get(user_id, project.id)

    async def update(self, user_id: str, project_id: str, project_update_args: ProjectUpdateArgs) -> bool:
        """Update an existing project repository."""
        existing_project = await self._get_orm(user_id, project_id)

        if not existing_project:
            return False

        for key, value in project_update_args.model_dump(mode="json", exclude_unset=True).items():
            setattr(existing_project, key, value)

        try:
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise e

        return True

    async def delete(self, user_id: str, project_id: str) -> bool:
        """Delete a project repository by its ID."""
        project = await self._get_orm(user_id, project_id)

        if not project:
            return False
        
        try:
            await self.db_session.delete(project)
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise e

        return True
