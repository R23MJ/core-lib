import uuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from core_lib.orm.base import Base

class UserORM(Base):
    '''User Model'''
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    oauth_provider = Column(String, nullable=False)

    encrypted_oauth_token = Column(String, nullable=False)
    encrypted_refresh_token = Column(String, nullable=True)
    oauth_token_expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP")

    projects = relationship("ProjectORM", back_populates="owner", cascade="all, delete-orphan")
