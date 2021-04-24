from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp
from modules import keyboard
from database.user import check_user_and_chat
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

    # Установка состояния главного меню
    await States.MAIN_MENU.set()

    # Получение клавиатуры главного меню
    markup = await keyboard.get_keyboard(state)

    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=markup)
