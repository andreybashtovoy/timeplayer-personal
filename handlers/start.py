from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp
from modules import keyboard
from database.user import check_user
from states import States


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=keyboard.get_keyboard())

    await check_user(message.from_user.id, message.from_user.username)

    await States.MAIN_MENU.set()
