from fastapi import FastAPI, Depends
import uvicorn 
from sqlmodel import Session, text, select
from database import engine
from models import Habit

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

@app.post("/habit/form")
async def create_habit_form(
    name: str = Form(...),
    category: str | None = Form(None),
    session: Session = Depends(get_session)
): 
    # Check if habit with same name already exists
    statement = select(Habit).where(Habit.name == name)
    existing_habit = session.exec(statement).first()
    
    if existing_habit:
        raise HTTPException(status_code=400, detail="Habit with this name already exists")
    
    db_habit = Habit(
        name = name,
        category = category
    )
    session.add(db_habit)
    session.commit()
    session.refresh(db_habit)
    
    return RedirectResponse(url="/habits", status_code=303)

@app.get("/habits")
def habits_page(request: Request, session=Depends(get_session)):
    habits = session.exec(select(Habit)).all()
    return templates.TemplateResponse(
        "habits.html",
        {"request": request, "habits": habits}
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
