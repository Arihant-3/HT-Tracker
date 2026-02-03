from fastapi import APIRouter, Depends
from sqlmodel import Session, text, select
from app.models import User, Habit, HabitLog
from app.dependencies.auth import get_current_user

# For templates and forms
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Request, Form

templates = Jinja2Templates(directory="app/templates")

# Create a Router instance
router = APIRouter()

# Getting data models from schemas
import app.schemas as schemas

# Access data from the database(sql) for CRUD operations
from app.database import get_session


# Create habit via form
@router.post("/habit/form")
def create_habit(
    name: str = Form(...),
    current_user: User = Depends(get_current_user),
    category: str | None = Form(None),
    session: Session = Depends(get_session)
): 
    user_id = current_user.id
    
    # Check if habit with same name already exists
    stmt = select(Habit).where(Habit.name == name, Habit.user_id == user_id)
    existing_habit = session.exec(stmt).first()

    if existing_habit:
        response = RedirectResponse(url="/habits", status_code=303)
        response.set_cookie(key="flash", value="Habit with this name already exists", max_age=3)
        return response
        
    db_habit = schemas.HabitCreate(
        user_id = user_id,
        name = name,
        category = category
    )
    db_habit = Habit(**db_habit.model_dump())
    
    session.add(db_habit)
    session.commit()
    session.refresh(db_habit)

    return RedirectResponse(url=f"/habits", status_code=303)

# Guard route to prevent GET on habit/form
@router.get("/habit/form")
def habit_form_guard():
    return RedirectResponse("/habits", status_code=303)

@router.get("/habits")
def habits_page(
    request: Request, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    flash_message = request.cookies.get("flash")
    
    user_id = current_user.id
    username = session.get(User, user_id).username

    count_stmt = text("SELECT COUNT(*) FROM habit WHERE user_id = :user_id")
    total_habit = session.scalar(count_stmt, params={"user_id": user_id})

    count_log_per_habit = text('''SELECT h.id, h.name, h.category, COUNT(hl.id) AS log_count
                               FROM habit AS h
                               LEFT JOIN habitlog AS hl
                               ON h.id = hl.habit_id
                               WHERE h.user_id = :user_id
                               GROUP BY h.id, h.name, h.category
                               ''')
    habits = session.exec(count_log_per_habit, params={"user_id": user_id}).all()
    
    response = templates.TemplateResponse(
        "habits.html",
        {
            "request": request, 
            "habits": habits, 
            "total_habit": total_habit,
            "user_id": user_id,
            "username": username
        }
    )
    
    if flash_message:
        response.delete_cookie("flash")
        
    return response
    


# Delete a habit and its logs
@router.post("/habits/{habit_id}/delete")
def delete_habit(
    habit_id: int,
    session: Session = Depends(get_session)
):

    habit = session.get(Habit, habit_id)
    if not habit:
        response = RedirectResponse(url="/habits", status_code=303)
        response.set_cookie(key="flash", value="Habit not found", max_age=3)
        return response
    
    # Delete associated logs first
    logs = session.exec(select(HabitLog).where(HabitLog.habit_id == habit_id)).all()
    for log in logs:
        session.delete(log)
        
    session.delete(habit)
    session.commit()
    
    return RedirectResponse(url=f"/habits", status_code=303)

