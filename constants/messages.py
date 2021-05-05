from aiogram.utils.markdown import hitalic, hbold, text
from aiogram.utils.emoji import emojize

SELECTING_ACTIVITY = emojize('Выбери занятие, которое хочешь начать :arrow_down::arrow_down::arrow_down:')

SELECTING_SUBACTIVITY = emojize('Выбери подзанятие, которое хочешь начать :arrow_down::arrow_down::arrow_down:')

STARTED_ACTIVITY = text(
    emojize(':rocket: Ты начал(-a) занятие "'), hitalic('{activity_type_name}'), '".',
    sep=""
)

STARTED_SUBACTIVITY = text(
    text(
        emojize(':rocket: Ты начал(-a) занятие'), hitalic('{activity_type_name}')
    ),
    text(
        emojize(":open_file_folder: Подзанятие:"), hitalic('{subactivity_name}')
    ),
    sep="\n"
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

CURRENT_ACTIVITY = text(
    text(
        emojize(':dart:'), "Занятие:", hitalic('{activity_type_name}')
    ),
    text(
        emojize(':muscle:'), "С пользой:", hitalic('{with_benefit}')
    ),
    text(
        emojize(':stopwatch:'), "Потрачено времени:", hitalic('{hours} часов {minutes} минут {seconds} секунд')
    ),
    sep="\n"
)

REMOVED_ACTIVITY_TYPE = text(
    emojize(':heavy_check_mark:'),
    "Занятие успешно удалено.",
    "Чтобы восстановить занятие вместе со всем прогрессом, необходимо создать новое занятие с таким же названием."
)

SA_SELECTING_ACTIVITY = text(
    emojize(':arrow_down:'),
    "Выбери занятие, к которому хочешь посмотреть подзанятия"
)

SA_CURRENT_ACTIVITY = text(
    emojize(':arrow_down:'),
    "Здесь ты можешь создавать подзанятия для занятия", hitalic('{activity_type_name}')
)

CURRENT_SUBACTIVITY = text(
    text(
        emojize(':dart:'), "Занятие:", hitalic('{activity_type_name}')
    ),
    text(
        emojize(':muscle:'), "Подзанятие:", hitalic('{subactivity_name}')
    ),
    text(
        emojize(':stopwatch:'), "Потрачено времени:", hitalic('{hours} часов {minutes} минут {seconds} секунд')
    ),
    sep="\n"
)

REMOVED_SUBACTIVITY = text(
    emojize(':heavy_check_mark:'),
    "Подзанятие успешно удалено.",
    "Чтобы восстановить подзанятие вместе со всем прогрессом, необходимо создать новое подзанятие с таким же названием."
)
