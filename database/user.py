from .models import User, Chat, ChatXUser, ActivityType


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
    query = ChatXUser.query.where(ChatXUser.chat_id == chat_id and ChatXUser.user_id == user_id)
    chat_x_user_exists = await query.gino.first()

    if not chat_x_user_exists:
        await ChatXUser.create(
            chat_id=chat_id,
            user_id=user_id
        )


async def get_user_accessible_activity_types(user_id) -> list[ActivityType]:
    result = await ActivityType.query.gino.all()
    return result
