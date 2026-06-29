from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    sent_at = Column(DateTime, server_default=func.now(), nullable=False)
    email_sent = Column(Boolean, nullable=False)

