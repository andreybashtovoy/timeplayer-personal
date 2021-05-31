from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb
from .core import update_state_and_send



@dp.message_handler(
    state=[States.MY_ACTIVITIES, States.SELECTING_ACTIVITY, States.SA_SELECTING_ACTIVITY, States.SELECTING_SUBACTIVITY,
           States.AA_SELECTING_ACTIVITY, States.AA_SELECTING_SUBACTIVITY, States.AA_ENTER_DURATION],
    text=buttons.BACK)
async def back_to_main_manu(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.MAIN_MENU,
                                text=messages.MAIN_MENU)


@dp.message_handler(state=[States.ENTER_ACTIVITY_TYPE_NAME, States.SELECT_WITH_BENEFIT, States.CURRENT_ACTVITY_TYPE],
                    text=buttons.BACK)
async def back_to_my_activities(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.MY_ACTIVITIES,
                                text=messages.MY_ACTIVITIES)


@dp.message_handler(state=[States.SA_CURRENT_ACTIVITY], text=buttons.BACK)
async def back_to_my_sa_selecting_activity(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.SA_SELECTING_ACTIVITY,
                                text=messages.SA_SELECTING_ACTIVITY)


@dp.message_handler(state=[States.ENTER_PENALTY], text=buttons.BACK)
async def back_to_my_sa_selecting_activity(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.ACTIVE_ACTIVITY,
                                text=messages.ACTIVE_ACTIVITY)


@dp.message_handler(state=[States.ENTER_SUBACTIVITY_NAME, States.CURRENT_SUBACIVITY], text=buttons.BACK)
async def back_to_my_sa_current_activity(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Получаем данные пользователя

    text = messages.SA_CURRENT_ACTIVITY.format(
        activity_type_name=data.get('current_activity_type_name')
    )

    await update_state_and_send(message, state,
                                state=States.SA_CURRENT_ACTIVITY,
                                text=text)
