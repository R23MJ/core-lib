"""ProjectCreatedEvent.py"""

from core_lib.events.event import Event

class ProjectCreatedEvent(Event):
    """Event emitted when a project is created.

    This event contains the details of the project that was created.
    """
    def __init__(self, project_id: str) -> None:
        self._project_id = project_id

    @property
    def event_type(self) -> str:
        """The name of the event."""
        return "project.created"

    async def to_dict(self) -> dict:
        """Convert the event to a dictionary."""
        return {
            "project_id": self._project_id
        }
