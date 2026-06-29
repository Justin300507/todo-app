from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, ConfigDict
import time

from app.database import get_db
from app.models.users import User
from app.models.teams import Teams
from app.models.team_memberships import TeamMembership
from app.models.tasks import Task
from app.models.lists import Lists

stats_router = APIRouter()

class StatsSummary(BaseModel):
    total_users: int
    total_teams: int
    total_tasks: int
    total_lists: int

    model_config = ConfigDict(from_attributes=True)

# Simple in‑memory cache for 30 seconds
_STATS_CACHE: dict | None = None
_CACHE_TIMESTAMP: float = 0.0
_CACHE_TTL = 30  # seconds

def _compute_stats(db: Session) -> dict:
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_teams = db.query(func.count(Teams.id)).scalar() or 0
    total_tasks = db.query(func.count(Task.id)).scalar() or 0
    total_lists = db.query(func.count(Lists.id)).scalar() or 0
    return {
        "total_users": total_users,
        "total_teams": total_teams,
        "total_tasks": total_tasks,
        "total_lists": total_lists,
    }

@stats_router.get("/stats/summary", response_model=StatsSummary)
def get_stats_summary(db: Session = Depends(get_db)):
    global _STATS_CACHE, _CACHE_TIMESTAMP
    now = time.time()
    if _STATS_CACHE is not None and (now - _CACHE_TIMESTAMP) < _CACHE_TTL:
        return _STATS_CACHE
    stats = _compute_stats(db)
    _STATS_CACHE = stats
    _CACHE_TIMESTAMP = now
    return stats