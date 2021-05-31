from aiogram import types
from aiogram.dispatcher import FSMContext
import re
from datetime import timedelta

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb
from .core import update_state_and_send

from database import activities, user

from modules.timedelta_convert import td_to_dict


@dp.message_handler(state=States.MAIN_MENU, text=buttons.ADD_TIME)
async def aa_select_activity(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.AA_SELECTING_ACTIVITY,
                                text=messages.AA_SELECTING_ACTIVITY)


@dp.message_handler(state=States.AA_SELECTING_ACTIVITY)
async def aa_selected_activity(message: types.Message, state: FSMContext):
    # Получаем занятие с введенным именем
    activity_type = await activities.get_chat_activity_type_by_name(
        activity_name=message.text,
        chat_id=message.chat.id
    )

    if activity_type is not None:
        subactivities = await user.get_user_subactivities(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            activity_type_id=activity_type.id
        )

        # Сохраняем название занятия
        await state.update_data(
            current_activity_type_id=activity_type.id,
            current_activity_type_name=message.text
        )

        if len(subactivities) != 0:

            await States.AA_SELECTING_SUBACTIVITY.set()  # Устанавливаем состояние выбора подзанятия

            text = messages.AA_SELECTING_SUBACTIVITY

        else:
            await state.update_data(
                subactivity_id=None
            )

            await States.AA_ENTER_DURATION.set()  # Устанавливаем состояние ввода продолжительности

            text = messages.AA_ENTER_DURATION

        await update_state_and_send(message, state,
                                    text=text)


@dp.message_handler(state=States.AA_SELECTING_SUBACTIVITY, text=buttons.WITHOUT_SUBACTIVITY)
async def without_subactivity(message: types.Message, state: FSMContext):
    # Сохраняем данные подзанятия
    await state.update_data(
        subactivity_id=None
    )

    await update_state_and_send(message, state,
                                state=States.AA_ENTER_DURATION,
                                text=messages.AA_ENTER_DURATION)


@dp.message_handler(state=States.AA_SELECTING_SUBACTIVITY)
async def selected_subactivity(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Получаем данные пользователя

    # Получаем занятие с введенным именем
    subactivity = await user.get_user_subactivity_by_name(
        user_id=message.from_user.id,
        activity_type_id=data.get('current_activity_type_id'),
        name=message.text
    )

    if subactivity is not None:
        # Сохраняем данные подзанятия
        await state.update_data(
            subactivity_id=subactivity.id,
            subactivity_name=message.text
        )

        await update_state_and_send(message, state,
                                    state=States.AA_ENTER_DURATION,
                                    text=messages.AA_ENTER_DURATION)


@dp.message_handler(state=States.AA_ENTER_DURATION)
async def create_subactivity(message: types.Message, state: FSMContext):

    if message.text.isdigit():
        td = timedelta(minutes=int(message.text))
    elif re.search(r"^\d{1,2}:\d{1,2}$", message.text):
        r = re.search(r"^(\d{1,2}):(\d{1,2})$", message.text)

        td = timedelta(hours=int(r[1]), minutes=int(r[2]))
    else:
        return

    data = await state.get_data()  # Получаем данные пользователя

    await activities.add_activity(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        activity_type=data.get('current_activity_type_id'),
        subactivity_id=data.get('subactivity_id'),
        duration=td
    )

    await update_state_and_send(message, state,
                                state=States.MAIN_MENU,
                                text=messages.ACTIVITY_ADDED)
