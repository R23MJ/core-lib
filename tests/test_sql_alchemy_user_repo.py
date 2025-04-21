from unittest.mock import MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from core_lib.repos.user.sql_alchemy import SQLAlchemyUserRepository
from core_lib.domain import User, UserUpdateArgs, UserCreateArgs

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
    return SQLAlchemyUserRepository(mock_session)

@pytest.mark.asyncio
async def test_get_user_found(repo, mocker):
    mock_user = User(
        id="1",
        username="test_user",
        email="test@example.com",
        oauth_provider="test_provider",
        encrypted_oauth_token="encrypted_token",
        encrypted_refresh_token="encrypted_refresh_token",
        oauth_token_expires_at=None,
    )
    scalars_mock = MagicMock()
    scalars_mock.first.return_value = mock_user
    repo.db_session.execute.return_value = MagicMock(scalars=lambda: scalars_mock)

    result = await repo.get(user_id="123")

    assert isinstance(result, User)
    assert result.id == "1"
    assert result.username == "test_user"
    assert result.email == "test@example.com"
    assert result.oauth_provider == "test_provider"
    assert result.encrypted_oauth_token == "encrypted_token"
    assert result.encrypted_refresh_token == "encrypted_refresh_token"
    repo.db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_not_found(repo, mocker):
    scalars_mock = MagicMock()
    scalars_mock.first.return_value = None
    repo.db_session.execute.return_value = MagicMock(scalars=lambda: scalars_mock)

    result = await repo.get(user_id="1")
    assert result is None

@pytest.mark.asyncio
async def test_create_user(repo, mocker):

    def fake_refresh(instance):
        instance.id = "1"

    mock_user = User(
        id="1",
        username="test_user",
        email="test@example.com",
        oauth_provider="test_provider",
        encrypted_oauth_token="encrypted_token",
        encrypted_refresh_token="encrypted_refresh_token",
        oauth_token_expires_at=None,
    )

    mock_user_args = UserCreateArgs(
        username="test_user",
        email="test@example.com",
        oauth_provider="test_provider",
        encrypted_oauth_token="encrypted_token",
        encrypted_refresh_token="encrypted_refresh_token",
        oauth_token_expires_at=None,
    )

    repo.db_session.refresh = mocker.AsyncMock(side_effect=fake_refresh)
    repo.db_session.add = MagicMock()
    repo.db_session.commit = mocker.AsyncMock()

    mocker.patch.object(repo, "get", mocker.AsyncMock(return_value=mock_user))

    result = await repo.create(user_create_args=mock_user_args)

    repo.db_session.add.assert_called()
    repo.db_session.commit.assert_awaited_once()
    repo.db_session.refresh.assert_awaited_once()
    assert isinstance(result, User)
    assert result.id == "1"
    assert result.username == "test_user"
    assert result.email == "test@example.com"
    assert result.oauth_provider == "test_provider"
    assert result.encrypted_oauth_token == "encrypted_token"
    assert result.encrypted_refresh_token == "encrypted_refresh_token"

@pytest.mark.asyncio
async def test_update_user_success(repo, mocker):
    mock_user = MagicMock()
    repo._get_orm = mocker.AsyncMock(return_value=mock_user)
    repo.db_session.commit = mocker.AsyncMock()

    args = UserUpdateArgs(
        username="test_user",
        email="test@example.com",
        oauth_provider="test_provider",
        encrypted_oauth_token="encrypted_token",
        encrypted_refresh_token="encrypted_refresh_token",
    )

    result = await repo.update(user_id="42", user_update_args=args)

    assert result is True
    assert mock_user.username == "test_user"
    assert mock_user.email == "test@example.com"
    assert mock_user.oauth_provider == "test_provider"
    assert mock_user.encrypted_oauth_token == "encrypted_token"
    assert mock_user.encrypted_refresh_token == "encrypted_refresh_token"
    repo.db_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user_not_found(repo, mocker):
    repo._get_orm = mocker.AsyncMock(return_value=None)

    args = UserUpdateArgs(
        username="test_user",
        email="test@example.com",
        oauth_provider="test_provider",
        encrypted_oauth_token="encrypted_token",
        encrypted_refresh_token="encrypted_refresh_token",
        oauth_token_expires_at="2023-10-01T00:00:00Z",
    )

    result = await repo.update(user_id="42", user_update_args=args)

    assert result is False


@pytest.mark.asyncio
async def test_delete_user_success(repo, mocker):
    mock_user = MagicMock()
    repo._get_orm = mocker.AsyncMock(return_value=mock_user)

    result = await repo.delete(user_id="99")

    repo.db_session.delete.assert_awaited_once_with(mock_user)
    repo.db_session.commit.assert_awaited_once()
    assert result is True

@pytest.mark.asyncio
async def test_delete_user_not_found(repo, mocker):
    repo._get_orm = mocker.AsyncMock(return_value=None)

    result = await repo.delete(user_id="99")

    repo.db_session.delete.assert_not_called()
    assert result is False
