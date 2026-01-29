from fastapi import Depends, Request, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models import User


# MOST IMPORTANT:
# Dependency to get the current authenticated user

def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
) -> User:
    user_id = request.cookies.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    return user
