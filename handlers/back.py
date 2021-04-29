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


@dp.message_handler(state=[States.ENTER_ACTIVITY_TYPE_NAME, States.SELECT_WITH_BENEFIT], text=buttons.BACK)
async def back_to_my_activities(message: types.Message, state: FSMContext):
    await States.MY_ACTIVITIES.set()  # Устанавливаем состояние меню занятий пользователя

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.MAIN_MENU,
        reply_markup=keyboard
    )
