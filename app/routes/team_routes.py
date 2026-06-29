from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, status
from sqlalchemy.orm import Session
from typing import Optional, List, Dict

# Database dependency
from app.database import get_db

# Models
from app.models.teams import Teams

# Schemas for team create/update
from app.schemas.team import TeamCreate, TeamUpdate

# Auth utilities
from app.utils.auth import get_current_user, oauth2_scheme

team_router = APIRouter()

# ---------------------------------------------------------------------------
# Helper function to serialize a Teams ORM object into a plain dict
# ---------------------------------------------------------------------------
def _team_to_dict(team: Teams) -> Dict:
    """Convert a Teams ORM instance to a serializable dictionary.
    Adjust the fields below if the Teams model contains additional columns.
    """
    return {
        "id": team.id,
        "name": getattr(team, "name", None),
        "description": getattr(team, "description", None),
    }

# ---------------------------------------------------------------------------
# Team endpoints (all require authentication)
# ---------------------------------------------------------------------------
@team_router.get("/teams", response_model=dict)
def list_teams(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    query = db.query(Teams)
    if search:
        # Assume Teams has a column `name` that stores the team title
        query = query.filter(Teams.name.ilike(f"%{search}%"))
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    serialized_items = [_team_to_dict(team) for team in items]
    return {"items": serialized_items, "total": total}

@team_router.get("/teams/{team_id}", response_model=dict)
def get_team(
    team_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    team = db.query(Teams).filter(Teams.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Not found")
    return _team_to_dict(team)

@team_router.post("/teams", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_team(
    team_in: TeamCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    # Map schema fields to model columns (assuming Teams has `name` and `description`)
    team = Teams(name=team_in.title)
    db.add(team)
    db.commit()
    db.refresh(team)
    return _team_to_dict(team)

@team_router.put("/teams/{team_id}", response_model=dict)
def update_team(
    team_in: TeamUpdate,
    team_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    team = db.query(Teams).filter(Teams.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Not found")
    if team_in.title is not None:
        team.name = team_in.title
    if team_in.description is not None:
        team.description = team_in.description
    db.commit()
    db.refresh(team)
    return _team_to_dict(team)

@team_router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    team = db.query(Teams).filter(Teams.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(team)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
