from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List
from datetime import datetime, date

from app.database import get_db
from app.utils.auth import get_current_user, oauth2_scheme
from app.models.tasks import Task
from app.schemas.task import TaskBase, TaskCreate, TaskUpdate, TaskRead

task_router = APIRouter()

def get_task_or_404(task_id: int, db: Session) -> Task:
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@task_router.get("/tasks", response_model=dict)
def list_tasks(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    status: Optional[str] = Query(None, pattern="^(open|in_progress|completed)$"),
    assignee_id: Optional[int] = Query(None, ge=1),
    due_before: Optional[date] = Query(None),
    due_after: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    """Search and paginate tasks."""
    query = db.query(Task)

    filters: List = []
    if title:
        filters.append(Task.title.ilike(f"%{title}%"))
    if description:
        filters.append(Task.description.ilike(f"%{description}%"))
    if status:
        filters.append(Task.status == status)
    if assignee_id:
        filters.append(Task.assignee_id == assignee_id)
    if due_before:
        filters.append(Task.due_date <= due_before)
    if due_after:
        filters.append(Task.due_date >= due_after)

    if filters:
        query = query.filter(and_(*filters))

    total = db.query(func.count(Task.id)).filter(and_(*filters) if filters else True).scalar()

    tasks = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {
        "items": [
            TaskRead.model_validate(t, from_attributes=True).model_dump()
            for t in tasks
        ],
        "total": total,
    }

@task_router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    task = get_task_or_404(task_id, db)
    return TaskRead.model_validate(task, from_attributes=True)

@task_router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    new_task = Task(**task_in.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return TaskRead.model_validate(new_task, from_attributes=True)

@task_router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_in: TaskUpdate,
    task_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    task = get_task_or_404(task_id, db)
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return TaskRead.model_validate(task, from_attributes=True)

@task_router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    task = get_task_or_404(task_id, db)
    db.delete(task)
    db.commit()
    return None
