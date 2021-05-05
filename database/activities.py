from .models import Activity, ActivityType, ChatXActivityType, Subactivity
from .user import get_user_accessible_activity_types
from datetime import timedelta, datetime
from typing import Tuple
from sqlalchemy.sql.expression import literal_column
from sqlalchemy import and_

from .user import get_chat_activity_types


async def get_chat_activity_type_by_name(chat_id, activity_name) -> ActivityType:
    activity_types = await get_chat_activity_types(chat_id)

    for activity_type in activity_types:
        if activity_type.name == activity_name:
            return activity_type


async def start_activity_by_name(user_id, chat_id, activity_name) -> Activity:
    activity_type = await get_chat_activity_type_by_name(chat_id, activity_name)

    if activity_type is not None:
        activity = await start_activity(user_id, chat_id, activity_type.id)
        return activity


async def start_activity(user_id, chat_id, activity_type, subactivity_id=None) -> Activity:
    activity = await Activity.create(
        user_id=user_id,
        chat_id=chat_id,
        activity_type=activity_type,
        subactivity=subactivity_id
    )

    return activity


async def stop_activity(user_id, chat_id) -> Tuple[Activity, ActivityType]:
    activity, activity_type = None, None

    activities = await Activity.query.where(
        and_(Activity.user_id == user_id, Activity.chat_id == chat_id, Activity.duration == None)).gino.all()

    for activity in activities:
        duration = datetime.utcnow() - activity.start_time
        await activity.update(duration=duration).apply()

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


async def remove_activity_type(activity_type_id, chat_id):
    await ChatXActivityType.delete.where(
        and_(
            ChatXActivityType.activity_type == activity_type_id,
            ChatXActivityType.chat_id == chat_id
        )
    ).gino.status()


async def set_with_benefit(activity_type_id, chat_id, with_benefit):
    await ChatXActivityType.update.values(
        with_benefit=with_benefit
    ).where(
        and_(
            ChatXActivityType.activity_type == activity_type_id,
            ChatXActivityType.chat_id == chat_id
        )
    ).gino.status()


async def create_subactivity(activity_type_id, user_id, chat_id, name):
    result = await Subactivity.query.where(
        and_(
            Subactivity.activity_type == activity_type_id,
            Subactivity.user_id == user_id,
            Subactivity.chat_id == chat_id,
            Subactivity.name == name
        )
    ).gino.first()

    if result is None:
        await Subactivity.create(
            activity_type=activity_type_id,
            user_id=user_id,
            chat_id=chat_id,
            name=name
        )
    elif result.is_removed:
        await result.update(
            is_removed=False
        ).apply()


async def remove_subactivity(subactivity_id):
    await Subactivity.update.values(
        is_removed=True
    ).where(
        Subactivity.id == subactivity_id
    ).gino.status()
