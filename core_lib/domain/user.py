from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class User(BaseModel):
    """Project model for the application."""

    id: str
    username: str
    email: Optional[EmailStr]
    oauth_provider: str

    encrypted_oauth_token: str
    encrypted_refresh_token: Optional[str]
    oauth_token_expires_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
