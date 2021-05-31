from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from constants import buttons, messages, config
from loader import dp
from states import States
from keyboard import kb
from .core import update_state_and_send


@dp.message_handler(state=States.MAIN_MENU, text=buttons.MY_STATS)
async def my_stats(message: types.Message, state: FSMContext):

    text = messages.MY_STATS.format(
        link=f"{config.SERVER_URL}/user/{message.chat.id}/{message.from_user.id}"
    )

    await update_state_and_send(message, state,
                                text=text)
