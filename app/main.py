from fastapi import FastAPI, Depends
import uvicorn 
from datetime import date
from sqlmodel import Session, text, select, func
from database import engine
from models import Habit, HabitLog
from utils import stats_func as stats

# For templates and forms
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Request, Form, HTTPException

templates = Jinja2Templates(directory="templates")

# Create a FastAPI Instance
app = FastAPI()

# Getting data models from schemas
import schemas

# Access data from the database(sql) for CRUD operations
from database import get_session

# Define CRUD Endpoints
@app.get("/")
async def root():
    return {"message": "This is the example file of Habit-Time Tracker!"}

# Create habit via form
@app.post("/habit/form")
def create_habit(
    name: str = Form(...),
    category: str | None = Form(None),
    session: Session = Depends(get_session)
): 
    # Check if habit with same name already exists
    stmt = select(Habit).where(Habit.name == name)
    existing_habit = session.exec(stmt).first()
    
    if existing_habit:
        raise HTTPException(status_code=400, detail="Habit with this name already exists")
    
    db_habit = schemas.HabitCreate(
        name = name,
        category = category
    )
    db_habit = Habit(**db_habit.model_dump())
    
    session.add(db_habit)
    session.commit()
    session.refresh(db_habit)
    
    return RedirectResponse(url="/habits", status_code=303)


# Create habit via API
# @app.post("/habit")
# def create_habit_api(
#     habit: schemas.HabitCreate,
#     session: Session = Depends(get_session)
# ):
#     db_habit = Habit(**habit.model_dump())
#     session.add(db_habit)
#     session.commit()
#     session.refresh(db_habit)
#     return db_habit


@app.get("/habits")
def habits_page(request: Request, session: Session = Depends(get_session)):
    
    count_stmt = text("SELECT COUNT(*) FROM habit")
    total_habit = session.scalar(count_stmt)
    
    count_log_per_habit = text('''SELECT h.id, h.name, h.category, COUNT(hl.id) AS log_count
                               FROM habit AS h
                               LEFT JOIN habitlog AS hl
                               ON h.id = hl.habit_id
                               GROUP BY h.id, h.name, h.category
                               ''')
    habits = session.exec(count_log_per_habit)
    
    return templates.TemplateResponse(
        "habits.html",
        {
            "request": request, 
            "habits": habits, 
            "total_habit": total_habit
        }
    )

# Create habit log via form
@app.post("/habits/{habit_id}/form")
def create_habitlog(
    habit_id: int,
    value: int = Form(...),
    note: str | None = Form(None),
    session: Session = Depends(get_session)
):
    # Create the habit log entry for the given habit_id
    log = schemas.HabitLogCreate(
        habit_id = habit_id,
        date = date.today(),
        value = value,
        note = note
    )
    log = HabitLog(**log.model_dump())
    
    session.add(log)
    session.commit()
    session.refresh(log)
    
    return RedirectResponse(url=f"/habits/{habit_id}/log", status_code=303)

@app.get("/habits/{habit_id}/log")
def habitlog_page(
    habit_id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    logs = session.exec(select(HabitLog).where(HabitLog.habit_id == habit_id)).all()
    
    stmt = (
        select(
            HabitLog.date,
            func.sum(HabitLog.value).label("total_value")
        )
        .where(HabitLog.habit_id == habit_id)
        .group_by(HabitLog.date)
    )
    result = session.exec(stmt).all()
    grouped_logs = list(result)
    
    # Alternative raw SQL approach
    # stmt = text('''SELECT date, SUM(value) AS total_value 
    #                     FROM habitlog
    #                     WHERE habit_id = :habit_id
    #                     GROUP BY date''')
    # grouped_logs = session.exec(stmt.params(habit_id=habit_id))
    
    
    return templates.TemplateResponse(
        "logs.html",
        {
            "request": request, "habit": habit, 
            "logs": logs, 
            "grouped_logs": grouped_logs,
            
        }
    )

@app.get("/habits/{habit_id}/stats")
def get_stats(
    habit_id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    # Get habit details
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
  
    # Calculate weekly stats
    week_day = 7
    
    start_date_check = session.exec(
        select(func.min(HabitLog.date)).where(HabitLog.habit_id == habit_id)
    ).first()
    
    if not start_date_check or not stats.check_data_sufficiency(
        first_day=start_date_check, 
        required_days=week_day
    ):
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "habit": habit,
                "message": "Not enough data to generate stats. Please log data."
            }
        )
    
    daily_aggregations = stats.prepare_daily_aggregation_list(
        session=session,
        habit_id=habit_id,
        required_days=week_day
    )
    
    total_week = sum(da.total_minutes for da in daily_aggregations)
    avg_per_day = round(total_week / week_day, 2)
    
    weekly_stats = (schemas.WeeklyStats(
        habit_id=habit.id,
        habit_name=habit.name,
        daily=daily_aggregations,
        total_week=total_week,
        avg_per_day=avg_per_day
    ))
    
    return templates.TemplateResponse(
        "stats.html",
        {
            "request": request, "habit": habit,
            "weekly_stats": weekly_stats
        }
    )
    
    
    
# Delete everything for testing purpose
@app.delete("/delete_all")
def delete_all(session: Session = Depends(get_session)):
    session.exec(text("DELETE FROM habitlog"))
    session.exec(text("DELETE FROM habit"))
    
    session.commit()
    return {"message": "All data deleted successfully"}
    

# Run the FastAPI server
def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    
if __name__ == "__main__":
    main()
