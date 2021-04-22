from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

from modules import keyboard

from database.test import test


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=keyboard.get_keyboard())

    await test()
