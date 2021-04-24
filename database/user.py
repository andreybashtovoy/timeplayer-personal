from .models import User


async def check_user(user_id, username):
    exists = await User.query.where(User.username == username).gino.first()

    if not exists:
        await User.create(
            user_id=user_id,
            username=username
        )