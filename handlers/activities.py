from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import timedelta
from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb
from .core import update_state_and_send

from database import activities, user, stats

from modules.timedelta_convert import td_to_dict


@dp.message_handler(state=States.MAIN_MENU, text=buttons.START_ACTIVITY)
async def select_activity(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.SELECTING_ACTIVITY,
                                text=messages.SELECTING_ACTIVITY)


@dp.message_handler(state=States.SELECTING_ACTIVITY)
async def start_activity(message: types.Message, state: FSMContext):
    activity = await activities.start_activity_by_name(message.from_user.id, message.chat.id,
                                                       message.text)  # Запускаем занятие

    if activity is not None:
        await update_state_and_send(message, state,
                                    state=States.ACTIVE_ACTIVITY,
                                    text=messages.STARTED_ACTIVITY.format(
                                        activity_type_name=message.text
                                    ))


@dp.message_handler(state=States.MAIN_MENU, text=buttons.START_SUBACTIVITY)
async def select_subactivity(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.SELECTING_SUBACTIVITY,
                                text=messages.SELECTING_SUBACTIVITY)


@dp.message_handler(state=States.SELECTING_SUBACTIVITY)
async def start_subactivity(message: types.Message, state: FSMContext):
    subactivities = await user.get_all_user_subactivities(
        user_id=message.from_user.id,
        chat_id=message.chat.id
    )

    for subactivity in subactivities:
        if message.text == "%s (%s)" % (subactivity.name, subactivity.activity_name):
            await activities.start_activity(
                user_id=message.from_user.id,
                chat_id=message.from_user.id,
                activity_type=subactivity.activity_type,
                subactivity_id=subactivity.id
            )

            # Получаем текст сообщения и форматируем с названием занятия
            text = messages.STARTED_SUBACTIVITY.format(
                activity_type_name=subactivity.activity_name,
                subactivity_name=subactivity.name
            )

            await update_state_and_send(message, state,
                                        state=States.ACTIVE_ACTIVITY,
                                        text=text)
            break


@dp.message_handler(state=States.ACTIVE_ACTIVITY, text=buttons.STOP_ACTIVITY)
async def stop_activity(message: types.Message, state: FSMContext):
    activity, activity_type = await activities.stop_activity(message.from_user.id,
                                                             message.chat.id)  # Останавливаем занятие

    total_today = await stats.get_today_total_activity_duration(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        activity_type_id=activity.activity_type,
        subactivity_id=activity.subactivity
    )

    dict_total = td_to_dict(total_today)

    # Получаем текст сообщения и форматируем с названием занятия и продолжительностью
    text = messages.STOPPED_ACTIVITY.format(
        activity_type_name=activity_type.name,
        **td_to_dict(activity.duration),
        total_hours=dict_total['hours'],
        total_minutes=dict_total['minutes'],
        total_seconds=dict_total['seconds']
    )

    await update_state_and_send(message, state,
                                state=States.MAIN_MENU,
                                text=text)


@dp.message_handler(state=States.ACTIVE_ACTIVITY, text=buttons.STOP_PENALTY)
async def stop_penalty(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.ENTER_PENALTY,
                                text=messages.ENTER_PENALTY)


@dp.message_handler(state=States.ENTER_PENALTY)
async def entered_penalty(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        delta = timedelta(minutes=int(message.text))

        try:
            activity, activity_type = await activities.stop_activity(message.from_user.id,
                                                                 message.chat.id,
                                                                     delta=delta)  # Останавливаем занятие
        except Exception as e:
            await update_state_and_send(message, state,
                                        text=messages.PENALTY_ERROR)
            return

        text = messages.STOPPED_ACTIVITY.format(
            activity_type_name=activity_type.name,
            **td_to_dict(activity.duration)
        )

        await update_state_and_send(message, state,
                                    state=States.MAIN_MENU,
                                    text=text)


@dp.message_handler(state=States.ACTIVE_ACTIVITY, text=buttons.STATUS)
async def status(message: types.Message, state: FSMContext):
    # Получаем активное занятие пользователя и его продолжительность
    activity_type, duration = await user.get_user_active_activity(message.from_user.id, message.chat.id)

    # Получаем текст сообщения и форматируем с названием занятия и продолжительностью
    text = messages.STATUS.format(
        activity_type_name=activity_type.name,
        **td_to_dict(duration)
    )

    await update_state_and_send(message, state,
                                text=text)
