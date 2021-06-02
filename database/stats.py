from .models import Activity, ActivityType, ChatXActivityType
from .user import get_user_accessible_activity_types
from datetime import timedelta, datetime
from typing import Tuple
from sqlalchemy.sql.expression import literal_column
from sqlalchemy import and_
from sqlalchemy.sql.functions import func

from .loader import db

from dateutil import tz

local_tz = tz.gettz('Europe/Zaporozhye')


async def get_total_user_spent_time(user_id, chat_id, activity_type_id) -> timedelta:
    result = await db.select([func.sum(Activity.duration)]).where(
        and_(
            Activity.user_id == user_id,
            Activity.chat_id == chat_id,
            Activity.activity_type == activity_type_id
        )
    ).gino.scalar()

    if result is None:
        return timedelta()
    else:
        return result


async def get_total_user_spent_time_subactivity(user_id, chat_id, subactivity_id) -> timedelta:
    result = await db.select([func.sum(Activity.duration)]).where(
        and_(
            Activity.user_id == user_id,
            Activity.chat_id == chat_id,
            Activity.subactivity == subactivity_id
        )
    ).gino.scalar()

    if result is None:
        return timedelta()
    else:
        return result


async def get_today_total_activity_duration(user_id, chat_id, activity_type_id, subactivity_id) -> timedelta:
    result = await db.select([func.sum(Activity.duration)]).where(
        and_(
            Activity.user_id == user_id,
            Activity.chat_id == chat_id,
            Activity.activity_type == activity_type_id,
            Activity.subactivity == subactivity_id,
            Activity.start_time > datetime.combine(datetime.now(tz=local_tz).date(), datetime.min.time()).replace(
                tzinfo=local_tz).astimezone(tz=tz.UTC).replace(tzinfo=None),
            Activity.start_time < datetime.combine(datetime.now(tz=local_tz).date(), datetime.max.time()).replace(
                tzinfo=local_tz).astimezone(tz=tz.UTC).replace(tzinfo=None)
        )
    ).gino.scalar()

    return result
