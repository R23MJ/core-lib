import pytest
import aio_pika
from core_lib.events import RabbitMQFanOutEventEmitter, ProjectCreatedEvent

@pytest.mark.asyncio
async def test_emit_event_creates_exchange_and_publishes(mocker):
    mock_connection = mocker.Mock(spec=aio_pika.RobustConnection)
    mock_channel = mocker.AsyncMock()
    mock_exchange = mocker.AsyncMock()

    mock_connection.channel = mocker.AsyncMock(return_value=mock_channel)
    mock_channel.declare_exchange.return_value = mock_exchange

    emitter = RabbitMQFanOutEventEmitter(connection=mock_connection)
    event = ProjectCreatedEvent(project_id="123")

    await emitter.emit(event)

    mock_channel.declare_exchange.assert_awaited_once_with(
        event.event_type,
        aio_pika.ExchangeType.FANOUT,
        durable=True
    )
    mock_exchange.publish.assert_awaited_once()

@pytest.mark.asyncio
async def test_emit_event_uses_cached_exchange(mocker):
    mock_connection = mocker.Mock(spec=aio_pika.RobustConnection)
    mock_channel = mocker.AsyncMock()
    mock_exchange = mocker.AsyncMock()

    mock_connection.channel = mocker.AsyncMock(return_value=mock_channel)
    mock_channel.declare_exchange.return_value = mock_exchange

    emitter = RabbitMQFanOutEventEmitter(connection=mock_connection)
    event = ProjectCreatedEvent(project_id="123")

    await emitter.emit(event)

    mock_channel.declare_exchange.reset_mock()
    mock_exchange.publish.reset_mock()

    await emitter.emit(event)

    mock_channel.declare_exchange.assert_not_awaited()
    mock_exchange.publish.assert_awaited_once()
