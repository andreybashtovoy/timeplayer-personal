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


async def create_activity(user_id, chat_id, start_time, duration, activity_type_id, subactivity_id) -> Activity:
    activity = await Activity.create(
        user_id=user_id,
        chat_id=chat_id,
        activity_type=activity_type_id,
        subactivity=subactivity_id,
        start_time=start_time,
        duration=duration
    )

    return activity


async def remove_activity(activity_id):
    await Activity.delete.where(Activity.id == activity_id).gino.status()


async def edit_activity(activity_id, activity_type_id, subactivity_id, start_time, duration):
    await Activity.update.values(
        activity_type=activity_type_id,
        subactivity=subactivity_id,
        start_time=start_time,
        duration=duration
    ).where(
        Activity.id == activity_id
    ).gino.status()
