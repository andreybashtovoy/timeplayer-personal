import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram import types
from constants import buttons
from database import user
from .core import Keyboard
from states import States
from database.user import get_user_accessible_activity_types

kb = Keyboard()


@kb.with_state(state=States.MAIN_MENU)
async def main_menu_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
        one_time_keyboard=True,
        selective=True
    )

    markup.row(
        types.KeyboardButton(buttons.START_ACTIVITY),
        types.KeyboardButton(buttons.START_SUBACTIVITY)
    )

    markup.add(
        types.KeyboardButton(buttons.ADD_TIME)
    )

    markup.row(
        types.KeyboardButton(buttons.MY_ACTIVITIES),
        types.KeyboardButton(buttons.MY_SUBACTIVITIES)
    )

    markup.add(
        types.KeyboardButton(buttons.MY_STATS)
    )

    return markup


@kb.with_state(state=[States.SELECTING_ACTIVITY, States.SA_SELECTING_ACTIVITY, States.AA_SELECTING_ACTIVITY])
async def selecting_activity_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    activity_types = await user.get_chat_activity_types(message.chat.id)

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
        selective=True
    )

    markup.add(
        types.KeyboardButton(buttons.BACK)
    )

    for activity_type in activity_types:
        markup.add(
            types.KeyboardButton(activity_type.name)
        )

    return markup


@kb.with_state(state=States.SELECTING_SUBACTIVITY)
async def selecting_subactivity(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
        selective=True
    )

    markup.add(
        types.KeyboardButton(buttons.BACK)
    )

    subactivities = await user.get_all_user_subactivities(
        user_id=message.from_user.id,
        chat_id=message.chat.id
    )

    for subactivity in subactivities:
        markup.add(
            types.KeyboardButton("%s (%s)" % (subactivity.name, subactivity.activity_name))
        )

    return markup


@kb.with_state(state=States.AA_SELECTING_SUBACTIVITY)
async def selecting_subactivity_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
        selective=True
    )

    markup.row(
        types.KeyboardButton(buttons.WITHOUT_SUBACTIVITY),
        types.KeyboardButton(buttons.BACK)
    )

    data = await context.get_data()  # Получаем данные пользователя

    subactivities = await user.get_user_subactivities(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        activity_type_id=data.get('current_activity_type_id')
    )

    for subactivity in subactivities:
        markup.add(
            types.KeyboardButton(subactivity.name)
        )

    return markup


@kb.with_state(state=States.AA_ENTER_DURATION)
async def enter_duration_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True
    )

    markup.row(
        types.KeyboardButton(buttons.BACK)
    )

    return markup


@kb.with_state(state=States.ACTIVE_ACTIVITY)
async def active_activity_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True
    )

    markup.row(
        types.KeyboardButton(buttons.STOP_ACTIVITY),
        types.KeyboardButton(buttons.STATUS)
    )

    return markup


@kb.with_state(state=States.MY_ACTIVITIES)
async def my_activities_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True,
        row_width=1
    )

    markup.row(
        types.KeyboardButton(buttons.CREATE),
        types.KeyboardButton(buttons.BACK)
    )

    activity_types = await user.get_chat_activity_types(message.chat.id)

    for activity_type in activity_types:
        markup.add(
            types.KeyboardButton(activity_type.name)
        )

    return markup


@kb.with_state(state=[States.ENTER_ACTIVITY_TYPE_NAME, States.ENTER_ACTIVITY_TYPE_NAME])
async def enter_something(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True,
        row_width=1
    )

    markup.row(
        types.KeyboardButton(buttons.BACK)
    )

    return markup


@kb.with_state(state=States.SELECT_WITH_BENEFIT)
async def my_activities_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True,
        row_width=1
    )

    markup.row(
        types.KeyboardButton(buttons.YES),
        types.KeyboardButton(buttons.NO)
    )

    markup.row(
        types.KeyboardButton(buttons.BACK)
    )

    return markup


@kb.with_state(state=States.CURRENT_ACTVITY_TYPE)
async def current_activity_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True,
        row_width=1
    )

    data = await context.get_data()  # Получаем данные пользователя

    if data.get('current_activity_type_with_benefit'):
        markup.add(
            types.KeyboardButton(buttons.MAKE_WITHOUT_BENEFIT)
        )
    else:
        markup.add(
            types.KeyboardButton(buttons.MAKE_WITH_BENEFIT)
        )

    markup.add(
        types.KeyboardButton(buttons.REMOVE),
        types.KeyboardButton(buttons.BACK)
    )

    return markup


@kb.with_state(state=States.SA_CURRENT_ACTIVITY)
async def sa_current_activity_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True,
        row_width=1
    )

    markup.row(
        types.KeyboardButton(buttons.CREATE),
        types.KeyboardButton(buttons.BACK)
    )

    data = await context.get_data()  # Получаем данные пользователя

    subactivities = await user.get_user_subactivities(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        activity_type_id=data.get('current_activity_type_id')
    )

    for subactivity in subactivities:
        markup.add(
            types.KeyboardButton(subactivity.name)
        )

    return markup


@kb.with_state(state=States.CURRENT_SUBACIVITY)
async def current_subactivity(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        selective=True,
        row_width=1
    )

    markup.add(
        types.KeyboardButton(buttons.REMOVE),
        types.KeyboardButton(buttons.BACK)
    )

    return markup


