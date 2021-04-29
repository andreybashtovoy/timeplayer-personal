from aiogram.utils.markdown import hitalic, hbold, text
from aiogram.utils.emoji import emojize

SELECTING_ACTIVITY = emojize('Выбери занятие, которое хочешь начать :arrow_down::arrow_down::arrow_down:')

STARTED_ACTIVITY = text(
    emojize(':rocket: Ты начал(-a) занятие "'), hitalic('{activity_type_name}'), '".',
    sep=""
)

STOPPED_ACTIVITY = text(
    emojize(':white_check_mark: Занятие завершено ({activity_type_name})'),
    "",
    emojize(':stopwatch: Продолжительность {hours} часов {minutes} минут {seconds} секунд'),
    sep="\n"
)


STATUS = text(
    "🟢", hbold("{activity_type_name}"), hitalic("({hours} часов {minutes} минут {seconds} секунд)")
)

MY_ACTIVITIES = text(
    emojize(':arrow_down:'),
    "Здесь ты можешь смотреть свои личные занятия, настраивать их и создавать новые"
)


MAIN_MENU = text(
    emojize(':arrow_down:'),
    "Ты находишься в главном меню"
)


ENTER_ACTIVITY_TYPE_NAME = text(
    emojize(':lower_left_crayon:'),
    "Напиши название занятия"
)


IS_WITH_BENEFIT = text(
    "Занятие с пользой?"
)

ACTIVITY_TYPE_CREATED = text(
    emojize(':heavy_check_mark:'),
    "Занятие успешно добавлено"
)
