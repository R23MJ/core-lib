from typing import Any, Dict
from pydantic import BaseModel

class ProjectCreateArgs(BaseModel):
    '''Project Creation Args'''
    repo_url: str
    environment_variables: Dict[str, Any]
