from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters.state import State


class Keyboard:
    def __init__(self):
        self.handlers = {}

    async def get_keyboard(self, message: types.Message, context: FSMContext) -> types.ReplyKeyboardMarkup:
        state = await context.get_state()

        if state in self.handlers:
            for h in self.handlers[state]:
                result = await h(message, context)
                return result

    def with_state(self, state):
        def add_handler(state, handler):
            if state.state in self.handlers:
                self.handlers[state.state].append(handler)
            else:
                self.handlers[state.state] = [handler]

        def registerhandler(handler):
            if type(state) is State:
                add_handler(state, handler)
            elif type(state) is list:
                for s in state:
                    add_handler(s, handler)
            return handler

        return registerhandler
