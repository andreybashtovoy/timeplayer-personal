from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb

from database import activities


@dp.message_handler(state=States.MAIN_MENU, text=buttons.START_ACTIVITY)
async def start_activity(message: types.Message, state: FSMContext):
    await States.SELECTING_ACTIVITY.set()  # Устанавливаем состояние выбора занятия

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.SELECTING_ACTIVITY,
        reply_markup=keyboard
    )


@dp.message_handler(state=States.SELECTING_ACTIVITY)
async def select_activity(message: types.Message, state: FSMContext):
    activity = await activities.start_activity_by_name(message.from_user.id, message.text)  # Запускаем занятие

    if activity is not None:
        await States.ACTIVE_ACTIVITY.set()  # Устанавливаем состояние активного занятия

        keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

        # Получаем текст сообщения и форматируем с названием занятия
        text = messages.STARTED_ACTIVITY.format(
            activity_type_name=message.text
        )

        await message.reply(
            text=text,
            parse_mode=types.ParseMode.HTML,
            reply_markup=keyboard
        )
