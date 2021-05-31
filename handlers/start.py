from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp
from keyboard import kb
from database.user import check_user_and_chat, check_has_activities
from states import States
from .core import update_state_and_send


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    # Проверка, есть ли пользователь и чат в базе
    await check_user_and_chat(
        user_id=message.from_user.id,
        username=message.from_user.username,
        chat_id=message.chat.id,
        chat_name=message.chat.full_name
    )

    # Добавить чату занятия по умолчанию, если их нет
    await check_has_activities(
        chat_id=message.chat.id
    )

    await update_state_and_send(message, state,
                                state=States.MAIN_MENU,
                                text=f"Привет, {message.from_user.full_name}!")
