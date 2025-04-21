from pydantic import BaseModel

class UserUpdateArgs(BaseModel):
    '''User Update Args'''
    
    username: str
    email: str

    oauth_provider: str
    encrypted_oauth_token: str
    encrypted_refresh_token: str | None = None
    oauth_token_expires_at: str | None = None