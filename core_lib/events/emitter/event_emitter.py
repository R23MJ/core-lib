'''EventEmitter.py
This module defines an abstract base class for event emitters.'''

from abc import ABC, abstractmethod
from core_lib.events import Event

class EventEmitter(ABC):
    """Abstract base class for event emitters.

    This class defines the interface for an event emitter, which can register
    listeners and emit events to them.
    """

    @abstractmethod
    async def emit(self, event: Event) -> None:
        """Emit an event to all registered listeners.

        Args:
            event (str): The name of the event to emit.
            *args: Positional arguments to pass to the listeners.
            **kwargs: Keyword arguments to pass to the listeners.
        """
