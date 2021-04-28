from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp
from keyboard import kb
from database.user import check_user_and_chat, check_has_activities
from states import States


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

    # Установка состояния главного меню
    await States.MAIN_MENU.set()

    # Получение клавиатуры главного меню
    markup = await kb.get_keyboard(message, state)

    await message.reply(f"Привет, {message.from_user.full_name}!",
                        reply_markup=markup)
