from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb

from database import activities, user

from modules.timedelta_convert import td_to_dict


@dp.message_handler(state=States.MAIN_MENU, text=buttons.ADD_TIME)
async def select_activity(message: types.Message, state: FSMContext):
    await States.AA_SELECTING_ACTIVITY.set()  # Устанавливаем состояние выбора занятия

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.AA_SELECTING_ACTIVITY,
        reply_markup=keyboard
    )