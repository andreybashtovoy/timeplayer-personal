from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    MAIN_MENU = State()
    ACTIVE_ACTIVITY = State()
    SELECTING_ACTIVITY = State()
