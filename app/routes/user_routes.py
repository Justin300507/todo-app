from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from app.database import get_db
from app.models.users import User
from app.utils.auth import get_current_user, get_password_hash

from app.schemas.user import UserCreate, UserUpdate, UserRead

# ---------------------------------------------------------------------------
# Router definition
# ---------------------------------------------------------------------------
user_router = APIRouter()

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def _is_admin(user: User) -> bool:
    return getattr(user, "role", None) == "admin"

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@user_router.get("/users", response_model=Dict[str, Any])
def list_users(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
) -> Dict[str, Any]:
    """List users with pagination. Requires authentication (any logged‑in user)."""
    total = db.query(User).count()
    users = (
        db.query(User)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {"items": [UserRead.model_validate(u, from_attributes=True) for u in users], "total": total}

@user_router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
) -> UserRead:
    """Retrieve a single user by ID. Returns 404 if not found."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return UserRead.model_validate(user, from_attributes=True)

@user_router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
) -> UserRead:
    """Create a new user - admin only."""
    if not _is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    # Ensure email uniqueness
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        password_hash=hashed,
        full_name=user_in.full_name,
        role=user_in.role,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserRead.model_validate(new_user, from_attributes=True)

@user_router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_in: UserUpdate,
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
) -> UserRead:
    """Update user details - allowed for self or admin."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    if current_user.id != user_id and not _is_admin(current_user):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    if user_in.role is not None:
        user.role = user_in.role
    if user_in.password is not None:
        user.password_hash = get_password_hash(user_in.password)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user, from_attributes=True)

@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user),
) -> None:
    """Delete a user - admin only."""
    if not _is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(user)
    db.commit()
    return None
