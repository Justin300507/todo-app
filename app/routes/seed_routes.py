from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.users import User
from app.models.teams import Teams
from app.models.team_memberships import TeamMembership
from app.models.lists import Lists
from app.models.tasks import Task
from app.utils.auth import get_password_hash

seed_router = APIRouter()

@seed_router.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    """Populate the database with demo data.
    This endpoint is idempotent - repeated calls will not create duplicate records.
    """
    # ----- Users -----
    users_data = [
        {"email": "alex.chen@example.com", "full_name": "Alex Chen", "password": "Password123!"},
        {"email": "maria.garcia@example.com", "full_name": "Maria Garcia", "password": "Password123!"},
        {"email": "james.kim@example.com", "full_name": "James Kim", "password": "Password123!"},
        {"email": "lina.patel@example.com", "full_name": "Lina Patel", "password": "Password123!"},
        {"email": "omar.nadal@example.com", "full_name": "Omar Nadal", "password": "Password123!"},
    ]
    new_users = []
    for u in users_data:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            user = User(
                email=u["email"],
                full_name=u["full_name"],
                hashed_password=get_password_hash(u["password"]),
                is_active=True,
            )
            new_users.append(user)
    if new_users:
        db.add_all(new_users)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()

    # ----- Teams -----
    teams_data = [
        {"name": "Alpha Team"},
        {"name": "Beta Squad"},
        {"name": "Gamma Group"},
        {"name": "Delta Force"},
        {"name": "Epsilon Unit"},
    ]
    new_teams = []
    for t in teams_data:
        existing = db.query(Teams).filter(Teams.name == t["name"]).first()
        if not existing:
            team = Teams(name=t["name"])  # type: ignore[arg-type]
            new_teams.append(team)
    if new_teams:
        db.add_all(new_teams)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()

    # ----- Lists -----
    # Assume each team gets a default "Inbox" list.
    teams = db.query(Teams).all()
    new_lists = []
    for team in teams:
        existing = (
            db.query(Lists)
            .filter(Lists.team_id == team.id, Lists.name == "Inbox")
            .first()
        )
        if not existing:
            lst = Lists(name="Inbox", team_id=team.id)  # type: ignore[arg-type]
            new_lists.append(lst)
    if new_lists:
        db.add_all(new_lists)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()

    # ----- Team Memberships -----
    # Assign each user to the first team for demo purposes.
    first_team = db.query(Teams).first()
    if first_team:
        users = db.query(User).all()
        new_memberships = []
        for user in users:
            existing = (
                db.query(TeamMembership)
                .filter(TeamMembership.user_id == user.id, TeamMembership.team_id == first_team.id)
                .first()
            )
            if not existing:
                membership = TeamMembership(user_id=user.id, team_id=first_team.id)  # type: ignore[arg-type]
                new_memberships.append(membership)
        if new_memberships:
            db.add_all(new_memberships)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()

    # ----- Tasks -----
    tasks_data = [
        {
            "title": "Launch Q3 campaign",
            "description": "Prepare and launch the Q3 marketing campaign.",
            "status": "in_progress",
        },
        {
            "title": "Fix login bug",
            "description": "Resolve the authentication error on the login page.",
            "status": "completed",
        },
        {
            "title": "Update user onboarding",
            "description": "Refresh the onboarding flow with new UI components.",
            "status": "open",
        },
        {
            "title": "Conduct team retrospective",
            "description": "Hold a retrospective meeting for the sprint.",
            "status": "open",
        },
        {
            "title": "Prepare financial report",
            "description": "Compile the quarterly financial report.",
            "status": "in_progress",
        },
    ]
    # Assign tasks to the first user and first list if they exist.
    assignee = db.query(User).first()
    default_list = db.query(Lists).first()
    new_tasks = []
    for td in tasks_data:
        task = Task(
            title=td["title"],
            description=td["description"],
            status=td["status"],
            assignee_id=assignee.id if assignee else None,
            list_id=default_list.id if default_list else None,
        )  # type: ignore[arg-type]
        new_tasks.append(task)
    if new_tasks:
        db.add_all(new_tasks)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()

    return {"detail": "Database seeded successfully"}
