from unittest.mock import MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from core_lib.repos.project.sql_alchemy import SQLAlchemyProjectRepository
from core_lib.domain import Project, ProjectCreateArgs, ProjectUpdateArgs

@pytest.fixture
def mock_session(mocker):
    session = mocker.Mock(spec=AsyncSession)
    session.execute = mocker.AsyncMock()
    session.commit = mocker.AsyncMock()
    session.rollback = mocker.AsyncMock()
    session.refresh = mocker.AsyncMock()
    session.add = mocker.Mock()
    session.delete = mocker.AsyncMock()
    return session

@pytest.fixture
def repo(mock_session):
    return SQLAlchemyProjectRepository(mock_session)

@pytest.mark.asyncio
async def test_get_project_found(repo, mocker):
    mock_project = Project(id="1", repo_url="x", environment_variables={"key": "value"}, status="testings")
    scalars_mock = MagicMock()
    scalars_mock.first.return_value = mock_project
    repo.db_session.execute.return_value = MagicMock(scalars=lambda: scalars_mock)

    result = await repo.get(user_id="1", project_id="123")

    assert isinstance(result, Project)
    assert result.id == "1"
    repo.db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_project_not_found(repo, mocker):
    scalars_mock = MagicMock()
    scalars_mock.first.return_value = None
    repo.db_session.execute.return_value = MagicMock(scalars=lambda: scalars_mock)

    result = await repo.get(user_id="1", project_id="123")
    assert result is None

@pytest.mark.asyncio
async def test_get_all_projects(repo, mocker):
    project1 = Project(id="1", repo_url="a", environment_variables={"key": "value"}, status="testings")
    project2 = Project(id="2", repo_url="b", environment_variables={"key": "value"}, status="testings")
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = [project1, project2]
    repo.db_session.execute.return_value = MagicMock(scalars=lambda: scalars_mock)

    result = await repo.get_all(user_id="1")

    assert len(result) == 2
    assert isinstance(result[0], Project)

@pytest.mark.asyncio
async def test_create_project(repo, mocker):
    mock_project_args = ProjectCreateArgs(repo_url="https://test.com", environment_variables={})
    repo.db_session.refresh = mocker.AsyncMock()
    repo.db_session.add = MagicMock()
    repo.db_session.commit = mocker.AsyncMock()

    mocker.patch.object(repo, "get", mocker.AsyncMock(return_value=Project(id="123", user_id="1", repo_url="https://test.com", environment_variables={}, status="active")))

    result = await repo.create(user_id="1", project_create_args=mock_project_args)

    repo.db_session.add.assert_called()
    repo.db_session.commit.assert_awaited_once()
    repo.db_session.refresh.assert_awaited_once()
    assert isinstance(result, Project)
    assert result.id == "123"


@pytest.mark.asyncio
async def test_update_project_success(repo, mocker):
    mock_project = MagicMock()
    repo._get_orm = mocker.AsyncMock(return_value=mock_project)
    repo.db_session.commit = mocker.AsyncMock()

    args = ProjectUpdateArgs(environment_variables={"NEW": "VAR"})
    result = await repo.update(user_id="1", project_id="42", project_update_args=args)

    assert result is True
    assert mock_project.environment_variables == {"NEW": "VAR"}
    repo.db_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_project_not_found(repo, mocker):
    repo._get_orm = mocker.AsyncMock(return_value=None)

    result = await repo.update(user_id="1", project_id="42", project_update_args=ProjectUpdateArgs(environment_variables={"NEW": "VAR"}))

    assert result is False


@pytest.mark.asyncio
async def test_delete_project_success(repo, mocker):
    mock_project = MagicMock()
    repo._get_orm = mocker.AsyncMock(return_value=mock_project)

    result = await repo.delete(user_id="1", project_id="99")

    repo.db_session.delete.assert_awaited_once_with(mock_project)
    repo.db_session.commit.assert_awaited_once()
    assert result is True

@pytest.mark.asyncio
async def test_delete_project_not_found(repo, mocker):
    repo._get_orm = mocker.AsyncMock(return_value=None)

    result = await repo.delete(user_id="1", project_id="99")

    repo.db_session.delete.assert_not_called()
    assert result is False
