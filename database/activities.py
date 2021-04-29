from .models import Activity, ActivityType, ChatXActivityType
from .user import get_user_accessible_activity_types
from datetime import timedelta, datetime
from typing import Tuple
from sqlalchemy.sql.expression import literal_column
from sqlalchemy import and_

from .user import get_chat_activity_types


async def start_activity_by_name(user_id, chat_id, activity_name) -> Activity:
    activity_types = await get_chat_activity_types(chat_id)

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


async def create_activity_type(chat_id, name, with_benefit):
    activity_type = await ActivityType.query.where(ActivityType.name == name).gino.first()

    # Если типа занятия с таким названием ещё нет в базе, создаем его
    if activity_type is None:
        activity_type = await ActivityType.create(
            name=name
        )

    # Проверяем есть ли принадлежность этого занятия этому чату
    chat_x_activity_type = await ChatXActivityType.query.where(
        and_(
            ChatXActivityType.chat_id == chat_id,
            ChatXActivityType.activity_type == activity_type.id
        )
    ).gino.first()

    # Если нет, то создаём
    if chat_x_activity_type is None:
        chat_x_activity_type = await ChatXActivityType.create(
            chat_id=chat_id,
            activity_type=activity_type.id,
            with_benefit=with_benefit
        )

