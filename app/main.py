from fastapi import FastAPI
# Model imports
from app.models.teams import *  # noqa: F401
from app.models.team_memberships import *  # noqa: F401
from app.models.users import *  # noqa: F401
from app.models.tasks import *  # noqa: F401
from app.models.lists import *  # noqa: F401
from app.models.notifications import *  # noqa: F401

# Database import for metadata creation
from app.database import Base, engine

# Router imports
from app.routes.auth_routes import auth_router
from app.routes.team_routes import team_router
from app.routes.stats_routes import stats_router
from app.routes.seed_routes import seed_router
from app.routes.user_routes import user_router
from app.routes.task_routes import task_router
from app.routes.list_item_routes import list_item_router
from app.routes.notification_routes import notification_router

app = FastAPI()

# CORS (required for frontend access)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Router registrations
app.include_router(auth_router)
app.include_router(team_router)
app.include_router(stats_router)
app.include_router(seed_router)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(list_item_router)
app.include_router(notification_router)

# Health endpoint (required for deployment health checks)
@app.get("/health")
def health():
    return {"status": "ok"}
