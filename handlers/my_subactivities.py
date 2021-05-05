from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb

from database import activities, stats, user
from modules.timedelta_convert import td_to_dict


@dp.message_handler(state=States.MAIN_MENU, text=buttons.MY_SUBACTIVITIES)
async def sa_selecting_activity(message: types.Message, state: FSMContext):
    await States.SA_SELECTING_ACTIVITY.set()  # Устанавливаем состояние выбора занятия

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.SA_SELECTING_ACTIVITY,
        reply_markup=keyboard
    )


@dp.message_handler(state=States.SA_SELECTING_ACTIVITY)
async def sa_current_activity(message: types.Message, state: FSMContext):
    # Получаем занятие с введенным именем
    activity_type = await activities.get_chat_activity_type_by_name(
        activity_name=message.text,
        chat_id=message.chat.id
    )

    if activity_type is not None:
        await States.SA_CURRENT_ACTIVITY.set()  # Устанавливаем состояние просмотра подзанятий занятия

        # Сохраняем название занятия
        await state.update_data(
            current_activity_type_id=activity_type.id,
            current_activity_type_name=message.text
        )

        keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

        text = messages.SA_CURRENT_ACTIVITY.format(
            activity_type_name=message.text
        )

        await message.reply(
            text=text,
            reply_markup=keyboard,
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(state=States.SA_CURRENT_ACTIVITY, text=buttons.CREATE)
async def request_new_subactivity_name(message: types.Message, state: FSMContext):
    await States.ENTER_SUBACTIVITY_NAME.set()  # Устанавливаем состояние ожидания ввода названия подзанятия

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.ENTER_ACTIVITY_TYPE_NAME,
        reply_markup=keyboard
    )


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

    await States.SA_CURRENT_ACTIVITY.set()  # Устанавливаем состояние текущего подзанятий

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    text = messages.SA_CURRENT_ACTIVITY.format(
        activity_type_name=data.get('current_activity_type_name')
    )

    await message.reply(
        text=text,
        reply_markup=keyboard,
        parse_mode=types.ParseMode.HTML
    )


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
        await States.CURRENT_SUBACIVITY.set()  # Устанавливаем состояние просмотра подзанятия

        # Сохраняем данные подзанятия
        await state.update_data(
            subactivity_id=subactivity.id,
            subactivity_name=message.text
        )

        keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

        text = await get_current_subactivity_text(message, state)

        await message.reply(
            text=text,
            reply_markup=keyboard,
            parse_mode=types.ParseMode.HTML
        )


@dp.message_handler(state=States.CURRENT_SUBACIVITY, text=buttons.REMOVE)
async def remove_subactivity(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Получаем данные пользователя

    # Удаляем занятие
    await activities.remove_subactivity(
        data.get('subactivity_id')
    )

    await States.SA_CURRENT_ACTIVITY.set()  # Устанавливаем состояние просмотра подзанятий занятия

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.REMOVED_SUBACTIVITY,
        reply_markup=keyboard,
        parse_mode=types.ParseMode.HTML
    )
