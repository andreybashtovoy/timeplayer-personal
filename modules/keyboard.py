import logging

from aiogram import Bot, Dispatcher, executor, types
from constants import buttons


def get_keyboard() -> types.ReplyKeyboardMarkup:
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

