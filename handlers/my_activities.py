from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb
from .core import update_state_and_send

from database import activities, stats
from modules.timedelta_convert import td_to_dict


@dp.message_handler(state=States.MAIN_MENU, text=buttons.MY_ACTIVITIES)
async def my_activities(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.MY_ACTIVITIES,
                                text=messages.MY_ACTIVITIES)


@dp.message_handler(state=States.MY_ACTIVITIES, text=buttons.CREATE)
async def request_new_activity_name(message: types.Message, state: FSMContext):
    await update_state_and_send(message, state,
                                state=States.ENTER_ACTIVITY_TYPE_NAME,
                                text=messages.ENTER_ACTIVITY_TYPE_NAME)


@dp.message_handler(state=States.ENTER_ACTIVITY_TYPE_NAME)
async def save_name_and_ask_about_benefit(message: types.Message, state: FSMContext):
    # Сохраняем название занятия
    await state.update_data(
        activity_type_name=message.text
    )

    await update_state_and_send(message, state,
                                state=States.SELECT_WITH_BENEFIT,
                                text=messages.IS_WITH_BENEFIT)


@dp.message_handler(state=States.SELECT_WITH_BENEFIT, text=[buttons.YES, buttons.NO])
async def create_activity(message: types.Message, state: FSMContext):
    with_benefit = message.text == buttons.YES  # True если занятие с пользой, иначе False

    data = await state.get_data()  # Получаем данные пользователя

    # Создаём занятие в базе
    await activities.create_activity_type(
        chat_id=message.chat.id,
        name=data.get("activity_type_name"),
        with_benefit=with_benefit
    )

    await update_state_and_send(message, state,
                                state=States.MY_ACTIVITIES,
                                text=messages.ACTIVITY_TYPE_CREATED)


async def get_current_activity_text(message: types.Message, state: FSMContext) -> str:
    data = await state.get_data()  # Получаем данные пользователя

    spent_time = await stats.get_total_user_spent_time(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        activity_type_id=data.get('current_activity_type_id')
    )

    return messages.CURRENT_ACTIVITY.format(
        activity_type_name=data.get('current_activity_type_name'),
        with_benefit='Да' if data.get('current_activity_type_with_benefit') else 'Нет',
        **td_to_dict(spent_time)
    )


@dp.message_handler(state=States.MY_ACTIVITIES)
async def select_activity_type(message: types.Message, state: FSMContext):
    # Получаем занятие с введенным именем
    activity_type = await activities.get_chat_activity_type_by_name(
        activity_name=message.text,
        chat_id=message.chat.id
    )

    if activity_type is not None:
        await States.CURRENT_ACTVITY_TYPE.set()  # Устанавливаем состояние просмотра личных занятий

        # Сохраняем название занятия
        await state.update_data(
            current_activity_type_id=activity_type.id,
            current_activity_type_name=message.text,
            current_activity_type_with_benefit=activity_type.with_benefit,
        )

        text = await get_current_activity_text(message, state)

        await update_state_and_send(message, state,
                                    state=States.CURRENT_ACTVITY_TYPE,
                                    text=text)


@dp.message_handler(state=States.CURRENT_ACTVITY_TYPE, text=buttons.REMOVE)
async def remove_activity_type(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Получаем данные пользователя

    # Удаляем занятие в базе
    await activities.remove_activity_type(
        activity_type_id=data.get('current_activity_type_id'),
        chat_id=message.chat.id
    )

    await update_state_and_send(message, state,
                                state=States.MY_ACTIVITIES,
                                text=messages.REMOVED_ACTIVITY_TYPE)


@dp.message_handler(state=States.CURRENT_ACTVITY_TYPE, text=[buttons.MAKE_WITHOUT_BENEFIT, buttons.MAKE_WITH_BENEFIT])
async def toggle_with_benefit(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Получаем данные пользователя

    # Записываем новое значение with_benefit
    await activities.set_with_benefit(
        activity_type_id=data.get('current_activity_type_id'),
        chat_id=message.chat.id,
        with_benefit=message.text == buttons.MAKE_WITH_BENEFIT
    )

    text = await get_current_activity_text(message, state)
    # Обновляем данные
    await state.update_data(
        current_activity_type_with_benefit=message.text == buttons.MAKE_WITH_BENEFIT,
    )

    await update_state_and_send(message, state,
                                text=text)
