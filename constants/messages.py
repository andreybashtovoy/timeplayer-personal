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
