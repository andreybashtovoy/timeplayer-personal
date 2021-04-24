import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from constants import buttons

from states import States


async def get_keyboard(context: FSMContext) -> types.ReplyKeyboardMarkup:
    state = await context.get_state()

    if state is States.MAIN_MENU:

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

