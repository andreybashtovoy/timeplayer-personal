from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb


@dp.message_handler(state=States.MAIN_MENU, text=buttons.MY_ACTIVITIES)
async def my_activities(message: types.Message, state: FSMContext):
    await States.MY_ACTIVITIES.set()  # Устанавливаем состояние просмотра личных занятий

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.MY_ACTIVITIES,
        reply_markup=keyboard
    )


@dp.message_handler(state=States.MY_ACTIVITIES)
async def select_activity(message: types.Message, state: FSMContext):
    pass
