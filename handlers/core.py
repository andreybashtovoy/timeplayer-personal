from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State

from keyboard import kb


async def update_state_and_send(message: types.Message, context: FSMContext, text: str, state: State = None):
    if state is not None:
        await state.set()  # Устанавливем новое стостояние

    keyboard = await kb.get_keyboard(message, context)  # Получаем клавиатуру с текущим состоянием

    # Отправляем сообщение
    await message.reply(
        text=text,
        parse_mode=types.ParseMode.HTML,
        reply_markup=keyboard
    )
