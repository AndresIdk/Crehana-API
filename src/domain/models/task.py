from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.data.db_methods import Base, BaseModelMixin


class Task(Base, BaseModelMixin):
    __tablename__ = "tasks"

    id_task = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    completeness = Column(String, default="0%")

    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=True, default=None)
    id_list_task = Column(
        Integer,
        ForeignKey("list_tasks.id_list_task", onupdate="CASCADE", ondelete="CASCADE"),
    )

    user = relationship("User", back_populates="tasks")
    list_task = relationship("ListTask", back_populates="tasks", passive_deletes=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
