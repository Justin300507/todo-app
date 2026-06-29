from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.database import get_db
from app.utils.auth import get_current_user
from app.models.notification import Notification
from app.schemas.notification import NotificationBase, NotificationCreate, NotificationUpdate, NotificationRead, NotificationListResponse

notification_router = APIRouter()

# Endpoints
@notification_router.get("/notifications", response_model=NotificationListResponse)
def list_notifications(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    total = (
        db.query(func.count(Notification.id))
        .filter(Notification.user_id == current_user.id)
        .scalar()
    )
    items = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {"items": items, "total": total}

@notification_router.get("/notifications/{notification_id}", response_model=NotificationRead)
def get_notification(
    notification_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == current_user.id)
        .first()
    )
    if not notification:
        raise HTTPException(status_code=404, detail="Not found")
    return notification

@notification_router.post("/notifications", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
def create_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    notification = Notification(**payload.dict(), user_id=current_user.id)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

@notification_router.put("/notifications/{notification_id}", response_model=NotificationRead)
def update_notification(
    payload: NotificationUpdate,
    notification_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == current_user.id)
        .first()
    )
    if not notification:
        raise HTTPException(status_code=404, detail="Not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(notification, field, value)
    db.commit()
    db.refresh(notification)
    return notification

@notification_router.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == current_user.id)
        .first()
    )
    if not notification:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(notification)
    db.commit()
    return
