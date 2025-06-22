from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.data.db_methods import Base, BaseModelMixin


class ListTask(Base, BaseModelMixin):
    __tablename__ = "list_tasks"

    id_list_task = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    tasks = relationship(
        "Task",
        back_populates="list_task",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
