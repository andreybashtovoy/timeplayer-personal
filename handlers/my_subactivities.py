from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb
from .core import update_state_and_send

from database import activities, stats, user
from modules.timedelta_convert import td_to_dict


@dp.message_handler(state=States.MAIN_MENU, text=buttons.MY_SUBACTIVITIES)
async def sa_selecting_activity(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.SA_SELECTING_ACTIVITY,
                                text=messages.SA_SELECTING_ACTIVITY)


@dp.message_handler(state=States.SA_SELECTING_ACTIVITY)
async def sa_current_activity(message: types.Message, state: FSMContext):
    # Получаем занятие с введенным именем
    activity_type = await activities.get_chat_activity_type_by_name(
        activity_name=message.text,
        chat_id=message.chat.id
    )

    if activity_type is not None:
        # Сохраняем название занятия
        await state.update_data(
            current_activity_type_id=activity_type.id,
            current_activity_type_name=message.text
        )

        text = messages.SA_CURRENT_ACTIVITY.format(
            activity_type_name=message.text
        )

        await update_state_and_send(message, state,
                                    state=States.SA_CURRENT_ACTIVITY,
                                    text=text)


@dp.message_handler(state=States.SA_CURRENT_ACTIVITY, text=buttons.CREATE)
async def request_new_subactivity_name(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.ENTER_SUBACTIVITY_NAME,
                                text=messages.ENTER_SUBACTIVITY_TYPE_NAME)


@dp.message_handler(state=States.ENTER_SUBACTIVITY_NAME)
async def create_subactivity(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Получаем данные пользователя

    # Создаем подзанятие
    await activities.create_subactivity(
        activity_type_id=data.get('current_activity_type_id'),
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        name=message.text
    )

    text = messages.SA_CURRENT_ACTIVITY.format(
        activity_type_name=data.get('current_activity_type_name')
    )

    await update_state_and_send(message, state,
                                state=States.SA_CURRENT_ACTIVITY,
                                text=text)


async def get_current_subactivity_text(message: types.Message, state: FSMContext) -> str:
    data = await state.get_data()  # Получаем данные пользователя

    spent_time = await stats.get_total_user_spent_time_subactivity(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        subactivity_id=data.get('subactivity_id')
    )

    return messages.CURRENT_SUBACTIVITY.format(
        activity_type_name=data.get('current_activity_type_name'),
        subactivity_name=message.text,
        **td_to_dict(spent_time)
    )


@dp.message_handler(state=States.SA_CURRENT_ACTIVITY)
async def current_subactivity(message: types.Message, state: FSMContext):
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

        text = await get_current_subactivity_text(message, state)

        await update_state_and_send(message, state,
                                    state=States.CURRENT_SUBACIVITY,
                                    text=text)


@dp.message_handler(state=States.CURRENT_SUBACIVITY, text=buttons.REMOVE)
async def remove_subactivity(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Получаем данные пользователя

    # Удаляем занятие
    await activities.remove_subactivity(
        data.get('subactivity_id')
    )

    await update_state_and_send(message, state,
                                state=States.SA_CURRENT_ACTIVITY,
                                text=messages.REMOVED_SUBACTIVITY)