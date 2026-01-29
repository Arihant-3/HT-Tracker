# Helper functions for statistics
from datetime import date, timedelta

def generate_date_range(start_date: date, end_date: date):
    """Generate a list of dates from start_date to end_date inclusive."""
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

def check_data_sufficiency(first_day: date, required_days: int) -> bool:
    """Check if there is sufficient data from start_date to today."""
    today = date.today()
    
    if today - first_day < timedelta(days=required_days - 1):
        return False
    return True

def prepare_daily_aggregation_list(
    session, 
    habit_id: int,
    user_id: int,
    required_days: int, 
    end_date: date = date.today()
):
    """Prepare a list of DailyAggregation for the past required_days."""
    from app.schemas import DailyAggregation
    from datetime import timedelta
    from sqlmodel import select, func
    from app.models import HabitLog
    
    start_date = end_date - timedelta(days=required_days - 1)
    
    stmt = (
        select(
            HabitLog.date,
            func.sum(HabitLog.value).label("total_minutes")
        )
        .where(
            (HabitLog.habit_id == habit_id) &
            (HabitLog.user_id == user_id) &
            (HabitLog.date >= start_date) &
            (HabitLog.date <= end_date)
        )
        .group_by(HabitLog.date)
    )
    result = session.exec(stmt).all()
    
    start_date = date.today() - timedelta(days=required_days - 1)
    daily_aggregations = []
    date_set = {record.date: record.total_minutes for record in result}
    
    for i in range(required_days):
        current_date = start_date + timedelta(days=i)
        total_minutes = date_set.get(current_date, 0)
        daily_aggregations.append(
            DailyAggregation(date=current_date, total_minutes=total_minutes)
        )
    
    return daily_aggregations