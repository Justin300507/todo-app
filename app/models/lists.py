from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Lists(Base):
    __tablename__ = "lists"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    order_index = Column(Integer, nullable=False)

