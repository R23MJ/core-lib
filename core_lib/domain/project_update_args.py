from typing import Any, Optional
from pydantic import BaseModel

class ProjectUpdateArgs(BaseModel):
    environment_variables: Optional[dict[str, Any]]
