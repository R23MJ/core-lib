import enum
import uuid
from sqlalchemy import JSON, Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from core_lib.orm.base import Base

class StatusORM(enum.Enum):
    '''Project Status Enum'''
    BUILDING = "building"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"

class ProjectORM(Base):
    '''Project Model'''
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    repo_url = Column(String, nullable=False)
    environment_variables = Column(JSON, nullable=True)
    status = Column(Enum(StatusORM), default=StatusORM.BUILDING, nullable=False)

    user_id = Column(String, ForeignKey("users.id"))

    owner = relationship("UserORM", back_populates="projects")
