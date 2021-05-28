from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb


@dp.message_handler(
    state=[States.MY_ACTIVITIES, States.SELECTING_ACTIVITY, States.SA_SELECTING_ACTIVITY, States.SELECTING_SUBACTIVITY,
           States.AA_SELECTING_ACTIVITY],
    text=buttons.BACK)
async def back_to_main_manu(message: types.Message, state: FSMContext):
    await States.MAIN_MENU.set()  # Устанавливаем состояние главного меню

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.MAIN_MENU,
        reply_markup=keyboard
    )


@dp.message_handler(state=[States.ENTER_ACTIVITY_TYPE_NAME, States.SELECT_WITH_BENEFIT, States.CURRENT_ACTVITY_TYPE],
                    text=buttons.BACK)
async def back_to_my_activities(message: types.Message, state: FSMContext):
    await States.MY_ACTIVITIES.set()  # Устанавливаем состояние меню занятий пользователя

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.MAIN_MENU,
        reply_markup=keyboard
    )


@dp.message_handler(state=[States.SA_CURRENT_ACTIVITY], text=buttons.BACK)
async def back_to_my_sa_selecting_activity(message: types.Message, state: FSMContext):
    await States.SA_SELECTING_ACTIVITY.set()  # Устанавливаем состояние выбора занятия

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.SA_SELECTING_ACTIVITY,
        reply_markup=keyboard
    )


@dp.message_handler(state=[States.ENTER_SUBACTIVITY_NAME, States.CURRENT_SUBACIVITY], text=buttons.BACK)
async def back_to_my_sa_current_activity(message: types.Message, state: FSMContext):
    await States.SA_CURRENT_ACTIVITY.set()  # Устанавливаем состояние выбора занятия

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    data = await state.get_data()  # Получаем данные пользователя

    text = messages.SA_CURRENT_ACTIVITY.format(
        activity_type_name=data.get('current_activity_type_name')
    )

    await message.reply(
        text=text,
        reply_markup=keyboard,
        parse_mode=types.ParseMode.HTML
    )
