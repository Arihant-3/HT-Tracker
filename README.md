# **Habit & Time Tracker**

A simple, structured end-to-end project, developed day-by-day to learn backend architecture, database migrations, and full-stack integration.

This app will allow users to:

- Track daily habits
- Log time spent on each habit
- View weekly and monthly summaries
- Explore analytics & visualizations

---

## 🛠 Tech Stack

- **FastAPI** — Backend framework
- **SQLModel** — ORM + data models
- **SQLite** (dev) → **MySQL** (future)
- **Alembic** — Database migration system
- **Jinja2 Templates** — Simple HTML frontend

---

## 🚀 Running the Project

```bash
uvicorn app.main:app --reload
```

Apply migrations:

```bash
alembic upgrade head
```

---


## 📌 Project Goal

By the end of this mini-project, the aim is to have a clean, functional backend + simple frontend that demonstrates:

- API design
- Database modeling
- Server-side templating
- SQL aggregation
- Proper migration workflow
- FastAPI best practices

This README will be updated with a full explanation once development is complete.
