from fastapi import APIRouter, Depends
from sqlmodel import Session, text, select
from app.models import Habit

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


# Create habit via form
@router.post("/habit/form")
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



@router.get("/habits")
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
