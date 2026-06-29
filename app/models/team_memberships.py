from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class TeamMembership(Base):
    __tablename__ = "team_memberships"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String, nullable=False)
    joined_at = Column(DateTime, server_default=func.now(), nullable=False)
