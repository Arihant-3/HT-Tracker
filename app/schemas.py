from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List

class HabitCreate(BaseModel):
    name: str
    category: Optional[str] = None
    
class HabitRead(BaseModel):
    id: int
    
class HabitLogCreate(BaseModel):
    habit_id: int
    date: date
    value: int
    note: Optional[str] = None
    
    model_config = ConfigDict(
        json_encoders={date: lambda o: o.strftime("%Y-%m-%d")}
    )
    
# class HabitLogSession(BaseModel):
#     habit_id: int
#     started_at: datetime
#     ended_at: datetime
#     note: str | None = None
    
#     # calculate duration(computed field)
#     @property
#     def duration(self):
#         return self.ended_at - self.started_at
    

class HabitLogRead(BaseModel):
    id: int
    
class DailyAggregation(BaseModel):
    date: date
    total_minutes: int
    
    model_config = ConfigDict(
        json_encoders={date: lambda o: o.strftime("%Y-%m-%d")}
    )

class WeeklyStats(BaseModel):
    habit_id: int
    habit_name: str
    # daily aggregations for the last 7 days(fill 0 for missing days)
    daily: List[DailyAggregation]
    total_week: int
    avg_per_day: float
    

