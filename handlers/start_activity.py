from aiogram import types

from constants import buttons
from loader import dp
from states import States


@dp.message_handler(state=States.MAIN_MENU, text=buttons.START_ACTIVITY)
async def start_activity(message: types.Message):
    pass
