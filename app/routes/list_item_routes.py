from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.utils.auth import get_current_user, oauth2_scheme
from app.models.lists import Lists
from app.models.tasks import Task
from app.models.users import User
from app.models.teams import Teams

from pydantic import BaseModel, Field, ConfigDict

# Router variable must be named exactly as required
list_item_router = APIRouter()

class ListCreate(BaseModel):
    name: str = Field(min_length=1)
    team_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class ListUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    team_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class ListResponse(BaseModel):
    id: int
    name: str
    team_id: Optional[int] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

@list_item_router.get("/lists")
def get_lists(
    search: Optional[str] = Query(None),
    owner_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    """List task lists with optional search and owner filtering, paginated."""
    query = db.query(Lists)

    if owner_id is not None:
        query = query.filter((Lists.user_id == owner_id) | (Lists.team_id == owner_id))
    if search:
        query = query.filter(Lists.name.ilike(f"%{search}%"))

    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return {
        "items": [ListResponse.model_validate(item, from_attributes=True).model_dump() for item in items],
        "total": total,
    }

@list_item_router.get("/lists/{list_id}")
def get_list(
    list_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    lst = db.query(Lists).filter(Lists.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Not found")
    return ListResponse.model_validate(lst, from_attributes=True).model_dump()

@list_item_router.post("/lists")
def create_list(
    list_in: ListCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    new_list = Lists(
        name=list_in.name,
        user_id=current_user.id,
        team_id=list_in.team_id,
    )
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=ListResponse.model_validate(new_list, from_attributes=True).model_dump(),
    )

@list_item_router.put("/lists/{list_id}")
def update_list(
    list_in: ListUpdate,
    list_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user)):
    lst = db.query(Lists).filter(Lists.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Not found")
    if list_in.name is not None:
        lst.name = list_in.name
    if list_in.team_id is not None:
        lst.team_id = list_in.team_id
    db.commit()
    db.refresh(lst)
    return ListResponse.model_validate(lst, from_attributes=True).model_dump()

@list_item_router.delete("/lists/{list_id}")
def delete_list(
    list_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    lst = db.query(Lists).filter(Lists.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="Not found")
    # Delete related tasks first to avoid orphan records
    db.query(Task).filter(Task.list_id == list_id).delete()
    db.delete(lst)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
