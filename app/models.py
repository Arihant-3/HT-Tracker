from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: Optional[str] = None

class HabitLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int
    date: date
    value: int
    note: Optional[str] = None
    

