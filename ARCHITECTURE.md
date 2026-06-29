# Architecture — Todo App

## ER Diagram

```
┌─────────────────────┐
│ Lists               │
├─────────────────────┤
│ id         Integer ││
│ name       String  ││
│ owner_user_id Integer│
│ owner_team_id Integer│
│ created_at DateTime││
│ order_index Integer ││
└─────────────────────┘

┌─────────────────────┐
│ Notification        │
├─────────────────────┤
│ id         Integer ││
│ user_id    Integer ││
│ task_id    Integer ││
│ sent_at    DateTime││
│ email_sent Boolean ││
└─────────────────────┘

┌─────────────────────┐
│ Task                │
├─────────────────────┤
│ id         Integer ││
│ title      String  ││
│ description Text    ││
│ due_date   DateTime││
│ status     String  ││
│ assignee_id Integer ││
│ list_id    Integer ││
│ order_index Integer ││
│ ... (2 more)    │
└─────────────────────┘

┌─────────────────────┐
│ TeamMembership      │
├─────────────────────┤
│ id         Integer ││
│ team_id    Integer ││
│ user_id    Integer ││
│ role       String  ││
│ joined_at  DateTime││
└─────────────────────┘

┌─────────────────────┐
│ Teams               │
├─────────────────────┤
│ id         Integer ││
│ name       String  ││
│ created_at DateTime││
└─────────────────────┘

┌─────────────────────┐
│ User                │
├─────────────────────┤
│ id         Integer ││
│ email      String  ││
│ hashed_password Strin│
│ full_name  String  ││
│ is_active  Boolean ││
│ role       String  ││
└─────────────────────┘

```

## Backend Architecture

```
FastAPI Application
├── Routing Layer (app/routes/)     → HTTP request handling
├── Service Layer (app/services/)   → Business logic
├── Model Layer (app/models/)       → Database ORM (SQLAlchemy)
├── Schema Layer (app/schemas/)     → Validation (Pydantic v2)
└── Database (app/database.py)      → Session management (SQLite)
```

## Design Patterns

- **Repository pattern**: services own DB queries, routes own HTTP logic
- **Dependency injection**: `get_db` session injected via FastAPI `Depends()`
- **Schema separation**: ORM models never exposed directly; Pydantic schemas serialize responses
- **JWT auth**: Bearer tokens validated via `oauth2_scheme` dependency
