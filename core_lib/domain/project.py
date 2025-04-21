from typing import Any, Dict
from pydantic import BaseModel, ConfigDict

class Project(BaseModel):
    """Project model for the application."""

    id: str
    repo_url: str
    environment_variables: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)
