from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb


@dp.message_handler(state=[States.MY_ACTIVITIES, States.SELECTING_ACTIVITY], text=buttons.BACK)
async def back_to_main_manu(message: types.Message, state: FSMContext):
    await States.MAIN_MENU.set()  # Устанавливаем состояние главного меню

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.MAIN_MENU,
        reply_markup=keyboard
    )
