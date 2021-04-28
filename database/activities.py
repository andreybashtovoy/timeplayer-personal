from .models import Activity, ActivityType
from .user import get_user_accessible_activity_types
from datetime import timedelta, datetime
from typing import Tuple
from sqlalchemy.sql.expression import literal_column
from sqlalchemy import and_


async def start_activity_by_name(user_id, chat_id, activity_name) -> Activity:
    activity_types = await get_user_accessible_activity_types(user_id)

    activity_type_id = None

    for activity_type in activity_types:
        if activity_type.name == activity_name:
            activity_type_id = activity_type.id
            break

    if activity_type_id is not None:
        activity = await start_activity(user_id, chat_id, activity_type_id)
        return activity


async def start_activity(user_id, chat_id, activity_type) -> Activity:
    activity = await Activity.create(
        user_id=user_id,
        chat_id=chat_id,
        activity_type=activity_type
    )

    return activity


async def stop_activity(user_id, chat_id) -> Tuple[Activity, ActivityType]:
    activity, activity_type = None, None

    activities = await Activity.query.where(and_(Activity.user_id == user_id, Activity.chat_id == chat_id, Activity.duration == None)).gino.all()

    for activity in activities:
        duration = datetime.utcnow() - activity.start_time
        await activity.update(duration=duration).apply()

        activity = activity
        activity_type = await ActivityType.query.where(ActivityType.id == activity.activity_type).gino.first()

    return activity, activity_type
