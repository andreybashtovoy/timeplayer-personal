from .models import User, Chat, ChatXUser, ActivityType, Activity, ChatXActivityType
from sqlalchemy import and_
from typing import Tuple
from datetime import datetime, timedelta


async def check_user_and_chat(user_id, username, chat_id, chat_name):
    # Проверка есть ли пользователь в базе
    user_exists = await User.query.where(User.user_id == user_id).gino.first()

    if not user_exists:
        await User.create(
            user_id=user_id,
            username=username
        )

    # Проверка есть ли чат в базе
    chat_exists = await Chat.query.where(Chat.chat_id == chat_id).gino.first()

    if not chat_exists:
        await Chat.create(
            chat_id=chat_id,
            name=chat_name
        )

    # Проверка есть ли соотношение чата и пользователя в базе
    query = ChatXUser.query.where(and_(ChatXUser.chat_id == chat_id, ChatXUser.user_id == user_id))
    chat_x_user_exists = await query.gino.first()

    if not chat_x_user_exists:
        await ChatXUser.create(
            chat_id=chat_id,
            user_id=user_id
        )


async def get_user_accessible_activity_types(user_id) -> list[ActivityType]:
    result = await ActivityType.query.gino.all()
    return result


async def get_chat_activity_types(chat_id) -> list[ActivityType]:
    results = await ChatXActivityType.__table__.join(ActivityType.__table__).select().where(
        ChatXActivityType.chat_id == chat_id).gino.all()
    return results


async def get_user_active_activity(user_id, chat_id) -> Tuple[ActivityType, timedelta]:
    activity = await Activity.query.where(
        and_(Activity.user_id == user_id, Activity.chat_id == chat_id, Activity.duration == None)).gino.first()

    if activity is not None:
        activity_type = await ActivityType.query.where(ActivityType.id == activity.activity_type).gino.first()

        duration = datetime.utcnow() - activity.start_time

        return activity_type, duration


async def check_has_activities(chat_id):
    chats_x_activity_types = await ChatXActivityType.query.where(ChatXActivityType.chat_id == chat_id).gino.all()

    if len(chats_x_activity_types) == 0:
        default_activity_types = await ActivityType.query.where(ActivityType.default == True).gino.all()

        for default_activity_type in default_activity_types:
            await ChatXActivityType.create(
                chat_id=chat_id,
                activity_type=default_activity_type.id,
                with_benefit=default_activity_type.with_benefit_default
            )
