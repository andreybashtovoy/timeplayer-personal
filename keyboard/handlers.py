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
        one_time_keyboard=True
    )

    markup.row(
        types.KeyboardButton(buttons.START_ACTIVITY),
        types.KeyboardButton(buttons.START_PROJECT)
    )

    markup.add(
        types.KeyboardButton(buttons.ADD_TIME),
        types.KeyboardButton(buttons.MY_ACTIVITIES),
        types.KeyboardButton(buttons.MY_STATS)
    )

    return markup


@kb.with_state(state=States.SELECTING_ACTIVITY)
async def selecting_activity_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    activity_types = await user.get_user_accessible_activity_types(message.from_user.id)

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1
    )

    for activity_type in activity_types:
        markup.add(
            types.KeyboardButton(activity_type.name)
        )

    return markup


@kb.with_state(state=States.ACTIVE_ACTIVITY)
async def active_activity_keyboard(message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.row(
        types.KeyboardButton(buttons.STOP_ACTIVITY),
        types.KeyboardButton(buttons.STATUS)
    )

    return markup
