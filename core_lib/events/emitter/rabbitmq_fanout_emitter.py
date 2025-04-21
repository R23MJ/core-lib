"""RabbitMQ Fanout Event Emitter"""

import aio_pika
from core_lib.events import Event
from . import EventEmitter

class RabbitMQFanOutEventEmitter(EventEmitter):
    """RabbitMQ implementation of the EventEmitter interface.

    This class provides methods for emitting events to RabbitMQ queues.
    """
    def __init__(self, connection: aio_pika.RobustConnection) -> None:
        self.connection = connection
        self.exchange_cache = {}

    async def emit(self, event: Event) -> None:
        """Emit an event to RabbitMQ."""

        channel = await self.connection.channel()

        if event.event_type not in self.exchange_cache:
            exchange = await channel.declare_exchange(
                event.event_type,
                aio_pika.ExchangeType.FANOUT,
                durable=True
            )
            self.exchange_cache[event.event_type] = exchange
        else:
            exchange = self.exchange_cache[event.event_type]

        await exchange.publish(
            aio_pika.Message(body=(await event.to_json()).encode()),
            routing_key=""
        )
