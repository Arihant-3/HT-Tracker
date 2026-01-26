from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    category: Optional[str] = None

class HabitLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habit.id")
    user_id: int = Field(foreign_key="user.id")
    date: date
    value: int
    note: Optional[str] = None
    
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    