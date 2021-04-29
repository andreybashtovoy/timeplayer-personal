from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    MAIN_MENU = State()
    ACTIVE_ACTIVITY = State()
    SELECTING_ACTIVITY = State()
    MY_ACTIVITIES = State()
    ENTER_ACTIVITY_TYPE_NAME = State()
    SELECT_WITH_BENEFIT = State()
