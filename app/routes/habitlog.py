from fastapi import APIRouter, Depends
from datetime import date
from sqlmodel import Session, select, func
from app.database import engine
from app.models import Habit, HabitLog
from app.utils import stats_func as stats

# For templates and forms
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Request, Form, HTTPException

templates = Jinja2Templates(directory="app/templates")

# Create a Router instance
router = APIRouter()

# Getting data models from schemas
import app.schemas as schemas

# Access data from the database(sql) for CRUD operations
from app.database import get_session


# Create habit log via form
@router.post("/habits/{habit_id}/form")
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

# View logs for a specific habit
@router.get("/habits/{habit_id}/log")
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
    
    return templates.TemplateResponse(
        "logs.html",
        {
            "request": request, "habit": habit, 
            "logs": logs, 
            "grouped_logs": grouped_logs,
            
        }
    )


# View weekly stats for a specific habit
@router.get("/habits/{habit_id}/stats")
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
    


# Delete a habit and its logs
@router.post("/habits/{habit_id}/delete")
def delete_habit(
    habit_id: int, 
    session: Session = Depends(get_session)
):
    habit = session.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Delete associated logs first
    logs = session.exec(select(HabitLog).where(HabitLog.habit_id == habit_id)).all()
    for log in logs:
        session.delete(log)
        
    session.delete(habit)
    session.commit()
    
    return RedirectResponse(url="/habits", status_code=303)

# Delete a specific log
@router.post("/logs/{log_id}/delete")
def delete_log(
    log_id: int,
    session: Session = Depends(get_session)
):
    log = session.get(HabitLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
        
    habit_id = log.habit_id
    session.delete(log)
    session.commit()
    
    return RedirectResponse(url=f"/habits/{habit_id}/log", status_code=303)
