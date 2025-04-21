from core_lib.events import Event
from . import EventEmitter

class NoopEventEmitter(EventEmitter):
    """No-op event emitter."""

    def __init__(self) -> None:
        """Initialize the NoopEventEmitter."""
        self.events = []

    async def emit(self, event: Event) -> None:
        """Emit an event to all registered listeners.

        Args:
            event (Event): The event to emit.
        """
        self.events.append(event)

    async def get_events(self) -> list[Event]:
        """Get the emitted events.

        Returns:
            list[Event]: The list of emitted events.
        """
        return self.events
