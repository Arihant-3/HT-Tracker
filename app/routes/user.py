from fastapi import APIRouter, Depends
from sqlmodel import Session, text, select
from app.models import User

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
    # stmt = select(User).where((User.username == username) | (User.email == email))
    # existing_user = session.exec(stmt).first()
    
    # if existing_user:
    #     raise HTTPException(status_code=400, detail="Username or email already exists")
    
    db_user = schemas.UserCreate(
        username=username,
        email=email,
        password=password
    )
    
    db_user = User(
        username=db_user.username,
        email=db_user.email,
        hashed_password=db_user.password  # In production, hash the password properly
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

