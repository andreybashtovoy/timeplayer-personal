from aiogram.utils.markdown import hitalic, text
from aiogram.utils.emoji import emojize

SELECTING_ACTIVITY = emojize('Выбери занятие, которое хочешь начать :arrow_down::arrow_down::arrow_down:')

STARTED_ACTIVITY = text(
    emojize(':rocket: Ты начал(-a) занятие "'), hitalic('{activity_type_name}'), '".',
    sep=""
)
