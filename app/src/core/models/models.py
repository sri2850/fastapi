from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.src.common.config.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    # hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1)

    # Establish relationships if required
    # For example, a user can have many tasks or projects:
    tasks = relationship("Task", back_populates="assignee")
    projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default = datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__: str = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    assignee_id = Column(Integer, ForeignKey("users.id"))
    assignee = relationship("Users", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
