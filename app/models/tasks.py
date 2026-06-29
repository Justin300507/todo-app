from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    order_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)
