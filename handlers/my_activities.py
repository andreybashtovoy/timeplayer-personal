from aiogram import types
from aiogram.dispatcher import FSMContext

from constants import buttons, messages
from loader import dp
from states import States
from keyboard import kb

from database import activities


@dp.message_handler(state=States.MAIN_MENU, text=buttons.MY_ACTIVITIES)
async def my_activities(message: types.Message, state: FSMContext):
    await States.MY_ACTIVITIES.set()  # Устанавливаем состояние просмотра личных занятий

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.MY_ACTIVITIES,
        reply_markup=keyboard
    )


@dp.message_handler(state=States.MY_ACTIVITIES, text=buttons.CREATE)
async def request_new_activity_name(message: types.Message, state: FSMContext):
    await States.ENTER_ACTIVITY_TYPE_NAME.set()  # Устанавливаем состояние ожидания ввода названия занятия

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.ENTER_ACTIVITY_TYPE_NAME,
        reply_markup=keyboard
    )


@dp.message_handler(state=States.ENTER_ACTIVITY_TYPE_NAME)
async def save_name_and_ask_about_benefit(message: types.Message, state: FSMContext):
    # Сохраняем название занятия
    await state.update_data(
        activity_type_name=message.text
    )

    await States.SELECT_WITH_BENEFIT.set()  # Устанавливаем состояние ожидания ответа, с пользой ли занятие

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.IS_WITH_BENEFIT,
        reply_markup=keyboard
    )


@dp.message_handler(state=States.SELECT_WITH_BENEFIT, text=[buttons.YES, buttons.NO])
async def create_activity(message: types.Message, state: FSMContext):
    with_benefit = message.text == buttons.YES  # True если занятие с пользой, иначе False

    data = await state.get_data()  # Получаем данные пользователя

    # Создаём занятие в базе
    await activities.create_activity_type(
        chat_id=message.chat.id,
        name=data.get("activity_type_name"),
        with_benefit=with_benefit
    )

    await States.MY_ACTIVITIES.set()  # Устанавливаем состояние просмотра личных занятий

    keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием

    await message.reply(
        text=messages.ACTIVITY_TYPE_CREATED,
        reply_markup=keyboard
    )



@dp.message_handler(state=States.MY_ACTIVITIES)
async def select_activity_type(message: types.Message, state: FSMContext):
    # activity_type = await activities.start_activity_by_name(message.from_user.id, message.chat.id,
    #                                                    message.text)  # Запускаем занятие
    #
    # if activity is not None:
    #     await States.ACTIVE_ACTIVITY.set()  # Устанавливаем состояние активного занятия
    #
    #     keyboard = await kb.get_keyboard(message, state)  # Получаем клавиатуру с текущим состоянием
    #
    #     # Получаем текст сообщения и форматируем с названием занятия
    #     text = messages.STARTED_ACTIVITY.format(
    #         activity_type_name=message.text
    #     )
    #
    #     await message.reply(
    #         text=text,
    #         parse_mode=types.ParseMode.HTML,
    #         reply_markup=keyboard
    #     )
    pass
