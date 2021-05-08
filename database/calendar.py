from .models import Activity, ActivityType, ChatXActivityType, Subactivity
from .user import get_user_accessible_activity_types
from datetime import timedelta, datetime
from typing import Tuple
from sqlalchemy.sql.expression import literal_column
from sqlalchemy import and_


async def get_user_activities(user_id, chat_id, from_date, to_date) -> list[Activity]:
    activities = await Activity.query.where(
        and_(
            Activity.user_id == user_id,
            Activity.chat_id == chat_id,
            Activity.start_time > from_date,
            Activity.start_time < to_date
        )
    ).gino.all()

    return activities
