from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    MAIN_MENU = State()
    ACTIVE_ACTIVITY = State()
    SELECTING_ACTIVITY = State()
    SELECTING_SUBACTIVITY = State()
    MY_ACTIVITIES = State()
    ENTER_ACTIVITY_TYPE_NAME = State()
    SELECT_WITH_BENEFIT = State()
    CURRENT_ACTVITY_TYPE = State()
    SA_SELECTING_ACTIVITY = State()
    SA_CURRENT_ACTIVITY = State()
    ENTER_SUBACTIVITY_NAME = State()
    CURRENT_SUBACIVITY = State()
