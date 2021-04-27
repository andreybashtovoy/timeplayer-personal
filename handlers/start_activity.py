from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb


@dp.message_handler(state=States.MAIN_MENU, text=buttons.START_ACTIVITY)
async def start_activity(message: types.Message, state: FSMContext):
    await States.SELECTING_ACTIVITY.set()  # Устанавливаем состояние выбора занятия

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.SELECTING_ACTIVITY,
        reply_markup=keyboard
    )
