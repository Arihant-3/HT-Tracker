from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models import User, Habit, HabitLog
from app.dependencies.auth import get_current_user
from app.utils.security import verify_password, hash_password

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

# Create/Register a new user

@router.post("/user/register/form")
def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """
    Create a new user.
    """
    # Check if username or email already exists
    stmt = select(User).where((User.username == username) | (User.email == email))
    existing_user = session.exec(stmt).first()
    
    if existing_user:
        return RedirectResponse(url="/user/register", status_code=303, 
                                headers={"X-Error": "Username or email already exists"})
    
    db_user = schemas.UserCreate(
        username=username,
        email=email,
        password=password
    )
    
    hashed = hash_password(db_user.password)
    
    db_user = User(
        username=db_user.username,
        email=db_user.email,
        hashed_password=hashed
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return RedirectResponse(url="/user/login", status_code=303)

@router.get("/user/register")
def get_user_registration(request: Request):
    return templates.TemplateResponse(
        "register.html", 
        {
            "request": request,
        }
    )


# User login
@router.get("/user/login")
def get_user(request: Request):
    return templates.TemplateResponse(
        "login.html", 
        {
            "request": request,
        }
    )
    
@router.post("/user/login/form")
def login_user(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """
    User login.
    """
    password_attempt = password
    
    stmt1 = select(User).where(User.email == email)
    user = session.exec(stmt1).first()
    
    if not user or not verify_password(password_attempt, user.hashed_password):
        return RedirectResponse(url="/user/login", status_code=303)
    
    # Adding cookie or session management can be done here
    response = RedirectResponse(url=f"/{user.id}/account", status_code=303)
    response.set_cookie(
        key="user_id", 
        value=str(user.id), 
        httponly=True
    )

    return response


@router.get("/{user_id}/account")
def get_account_page(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    User account page.
    """
    user_id = current_user.id
    
    user = session.get(User, user_id)
    if not user:
        return RedirectResponse(url="/user/login", status_code=303)

    username = user.username
    email = user.email 
    
    return templates.TemplateResponse(
        "account.html",
        {
            "request": request,
            "user_id": user_id,
            "username": username,
            "email": email
        }
    )

@router.post("/logout")
def logout_user():
    """
    User logout.
    """
    response = RedirectResponse(url="/user/login", status_code=303)
    response.delete_cookie(key="user_id")
    
    return response


# Delete the user
@router.post("/delete")
def delete_user(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a user and all associated habits and logs.
    """
    user_id = current_user.id
    
    user = session.get(User, user_id)
    if not user:
        return RedirectResponse(url="/user/login", status_code=303)
    
    # Delete associated habits and logs
    habits = session.exec(select(Habit).where(Habit.user_id == user_id)).all()
    for habit in habits:
        logs = session.exec(select(HabitLog).where(HabitLog.habit_id == habit.id)).all()
        for log in logs:
            session.delete(log)
        session.delete(habit)
        
    session.delete(user)
    session.commit()
    
    return RedirectResponse(url="/user/login", status_code=303)

