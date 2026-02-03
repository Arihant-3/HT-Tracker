# Habit & Time Tracker with Analytics

A backend-focused habit tracking application built with **FastAPI**, **SQLModel**, and **PostgreSQL**, designed to evolve from a single-user analytics system into a secure, multi-user, production-ready backend.

HT-Tracker emphasizes **clean backend architecture**, **relational data modeling**, **schema evolution**, and **auth-driven design** over frontend complexity.

---

## 🚀 What’s New in V2

HT-Tracker V2 is a **major architectural upgrade** over v1.

### Core Improvements

- Full **multi-user support**
- User authentication with **secure password hashing (Argon2)**
- Session-based authentication with HTTP-only cookies
- Per-user data isolation (`user_id` enforced at DB + route level)
- Modular FastAPI architecture using `APIRouter`
- Production-grade **PostgreSQL** / **MySQL** database
- Schema management via **Alembic**
- Hardened routing, auth flow, and UX feedback

V1 was intentionally frozen and shipped before introducing these changes.

---

## 🧠 Why This Project Exists

Most habit trackers stop at CRUD.

HT-Tracker goes deeper by focusing on:

- Relational modeling (`User -> Habit -> HabitLog`)
- Schema evolution and migrations
- Authentication boundaries
- Backend-driven UX decisions
- Defensive system design
- Shipping **real, complete versions**

V2 reflects how real backend systems grow -- by breaking, learning, and stabilizing.

---

## 🏗️ Architecture Overview (V2)

### Core Entities

**User**

- `id`
- `username`
- `email`
- `hashed_password`

**Habit**

- `id`
- `user_id`
- `name`
- `category`

**HabitLog**

- `id`
- `user_id`
- `habit_id`
- `date`
- `value` (minutes)
- `note` (optional)

### Relationships

```
User (1)
 ├── Habit (many)
       └── HabitLog (many)
 
```

All data access is scoped through the authenticated user.

---

## 🔐 Authentication & Security

- Passwords are **never stored in plain text**
- Password hashing uses **Argon2**
- Authentication is enforced via a centralized `get_current_user`
- Routes are fully protected (redirect-based, not raw 401s)
- Cookies are:
    - HTTP-only
    - Secure in production
    - Cleared cleanly on logout

Security decisions are explicit, not accidental.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **ORM:** SQLModel (SQLAlchemy)
- **Migrations:** Alembic
- **Database:** PostgreSQL / MySQL 8.0 (InnoDB, utf8mb4)
- **Auth:** Session-based (cookies)
- **Hashing:** Argon2
- **Templates:** Jinja2
- **Server:** Uvicorn + (Gunicorn recommended for higher concurrency)
- **Dependency Management:** uv

---

## ⚙️ Local Development

This project uses **uv** for dependency management.

### Setup

```bash
# install dependencies
uvsync

# apply migrations
alembic -c app/alembic.ini upgradehead

# start dev server
uvicorn app.main:app --reload

```

Open:

```
http://localhost:8000

```

```md
Optional (but nice):

> Note: You can also use `pip install -r requirements.txt` if you prefer pip.
```

---

## 🔐 Environment Variables

All sensitive configuration is environment-based.

```
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME

ENV=development | production
SECRET_KEY

```

> .env files are intentionally excluded from version control.
> 

---

## 🗄️ Database & Migrations

- Alembic is the **single source of truth** for schema changes
- `create_all()` is intentionally **not used**
- SQLite was used in v1; MySQL or PostgreSQL is the production target in v2
- Migration history was reset during the SQLite -> MySQL or PostgreSQL transition to ensure correctness

This mirrors real-world backend evolution.

---

## 🌍 Deployment

- Production runs via **uvicorn** (Gunicorn recommended for higher concurrency)
- MySQL/PostgreSQL credentials are injected via environment variables
- Static files are served by FastAPI
- Designed for deployment on platforms like **Render**

---

## 📦 Versioning

- **v1.0.0** -- Single-user, analytics-focused, SQLite
- **v2.0.0** -- Multi-user, authenticated, PostgreSQL-backed

Semantic versioning is followed strictly.

---

## 🎯 Key Learnings Demonstrated

- Relational data modeling
- Schema evolution & migrations
- Authentication design
- Secure password handling
- Route protection & UX alignment
- Environment-based configuration
- SQLite -> MySQL migration strategy and In production PostgreSQL
- Shipping stable versions


## 📌 Status

- ✅ V2.0.0 finalized
- 🔒 Secure by design
- 🧱 Clean migration baseline established

