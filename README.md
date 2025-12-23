# Habit & Time Tracker with Analytics

A backend-focused web application to track habits, log daily activity, and generate meaningful time-based analytics.

This project was built incrementally (day-by-day) with a strong emphasis on **backend architecture**, **relational data modeling**, and **SQL analytics**, rather than UI frameworks or authentication.

---

## 🚀 What This Project Does

- Create and manage habits
- Log daily activity (time spent in minutes)
- View recent logs and daily summaries
- Generate **weekly analytics**, including:
    - Total minutes logged (last 7 days)
    - Average minutes per day
    - Per-day breakdown (including zero-activity days)
- Gracefully handles edge cases (e.g. insufficient data)
- Clean, minimal UI with confirmation dialogs for destructive actions

---

## 🧠 Why This Project Exists

Most beginner projects stop at basic CRUD.

This project intentionally goes further by focusing on:

- Parent → child relational modeling
- SQL aggregation and analytics
- Time-windowed statistics
- Defensive backend programming
- Clean separation of concerns
- Shipping a complete, working system (v1)

Authentication and multi-user support are **intentionally deferred** to v2 to keep v1 focused and shippable.

---

## 🏗️ Architecture Overview

### Entities (v1)

**Habit**

- `id`
- `name`
- `category`

**HabitLog**

- `id`
- `habit_id`
- `date`
- `value` (minutes)
- `note` (optional)

Relationship:

```
Habit (1) → HabitLog (many)

```

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **ORM:** SQLModel
- **Migrations:** Alembic
- **Database:** SQLite (v1)
- **Templates:** Jinja2
- **Analytics:** SQL (`GROUP BY`, `SUM`, `COUNT`) + ORM functions
- **Frontend:** Server-rendered HTML + minimal CSS + vanilla JS

---

## 📊 Analytics & Stats (v1)

- Weekly stats are computed using a **7-day rolling window**
- Missing days are explicitly filled with `0` values
- Stats are only generated if sufficient data exists
- Analytics logic is isolated from routes for clarity and reuse

This ensures stats are **accurate, honest, and defensively computed**.

---

## ⚠️ Current Limitations (Intentional)

- Single-user only
- No authentication
- Data is global (not user-isolated)
- SQLite used for simplicity

These are **design decisions**, not missing features.

---

## 🔮 Planned v2 (Post-v1)

- Authentication (custom crypto-based or OAuth)
- User model and per-user data isolation
- `user_id` added to Habit and HabitLog
- Route modularization
- Optional DB upgrade (SQLite → MySQL/PostgreSQL)

v1 is frozen and released before starting v2.

---

## ▶️ Running Locally


This project uses **uv** for dependency management.

```bash
# install dependencies (using uv)
uv sync

# run migrations
alembic -c app/alembic.ini upgrade head

# start server
uvicorn main:app --reload

```

Then open:

```
http://localhost:8000

```

```md
Optional (but nice):

> Note: You can also use `pip install -r requirements.txt` if you prefer pip.
```

---

## 📦 Versioning

- **Current stable release:** `v1.0.0`
- Versioning follows semantic versioning
- v1 focuses on core system + analytics
- v2 will introduce authentication and multi-user support

---

## 🎯 Key Learnings Demonstrated

- Relational database modeling
- SQL aggregation and analytics
- Time-series data handling
- Defensive backend design
- Clean FastAPI architecture
- Shipping a complete product

---

## 📌 Status

- ✅ v1 complete and ready for deployment
- 🚧 v2 planned (authentication & multi-user)