"""Base class for events."""

from abc import ABC, abstractmethod
import json

class Event(ABC):
    """Abstract base class for events.

    This class defines the interface for an event, which can be emitted by an
    event emitter.
    """

    @property
    @abstractmethod
    def event_type(self) -> str:
        """The name of the event."""

    @abstractmethod
    async def to_dict(self) -> dict:
        """Convert the event to a dictionary."""

    async def to_json(self) -> str:
        """Convert the event to a JSON string."""
        return json.dumps(await self.to_dict())
