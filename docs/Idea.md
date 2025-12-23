# Habit & Time Tracker with Stats

## Version 1 (v1) — Single User, Core System

**What it is:**

A single-user habit and time tracking web application focused on backend architecture, relational data modeling, and analytics.

The goal of v1 is to design, build, and ship a complete system end-to-end (database → backend → UI → analytics → deployment) without authentication.

---

### Core Features

* Create and manage habits
* Log daily activity (time spent in minutes) per habit
* View recent logs and daily summaries
* Weekly analytics with:

  * Total minutes (last 7 days)
  * Daily averages
  * Per-day breakdown (including zero days)
* Defensive error handling when insufficient data exists
* Clean, minimal UI with confirmation dialogs for destructive actions

---

### Entities (v1)

* **Habit**

  * id
  * name
  * category

* **HabitLog**

  * id
  * habit_id
  * date
  * value (minutes)
  * note (optional)

---

### Backend (v1)

* FastAPI backend
* SQLModel ORM with Alembic migrations
* SQLite database (simple, zero-config for v1)
* Server-side rendered HTML using Jinja2
* Hybrid querying:

  * ORM for CRUD
  * SQL / aggregation functions for analytics

---

### Frontend (v1)

* `habits.html` — create & manage habits
* `habitlog.html` — log activity + view recent logs
* `stats.html` — weekly statistics & summaries
* `error.html` — graceful handling of edge cases

---

### What v1 Demonstrates

* Relational data modeling (parent → child)
* SQL aggregation & analytics (GROUP BY, SUM, COUNT)
* Time-windowed data analysis
* Defensive backend programming
* Clean separation of concerns
* Ability to ship a complete, working system

---

## Version 2 (v2) — Authentication & Multi-User System (Planned)

v2 will evolve the application into a multi-user system with proper authentication and data isolation.

---

### Planned Features (v2)

* User authentication (custom crypto-based auth or OAuth)
* Per-user habits and logs
* Secure password handling & hashing
* User-specific analytics and stats
* Optional database upgrade (SQLite → MySQL/PostgreSQL)
* Route modularization (routers per domain)

---

### New / Updated Entities (v2)

* **User**

  * id
  * email / username
  * password_hash
  * created_at

* **Habit**

  * id
  * user_id (FK → User)
  * name
  * category

* **HabitLog**

  * id
  * user_id (FK → User)
  * habit_id (FK → Habit)
  * date
  * value
  * note

---

### Backend Evolution (v2)

* Authentication middleware
* Authorization checks on all routes
* Stats filtered by user context
* Database-level integrity with foreign keys
* Scalable architecture for multiple users

---

### Long-Term Direction

* v1 focuses on **architecture, analytics, and shipping**
* v2 focuses on **security, users, and scalability**
* v3+ may explore advanced analytics, visualization, or encryption-heavy features

---

**Status:**

* v1: Complete and ready for deployment
* v2: Planned (post-deployment upgrade)
