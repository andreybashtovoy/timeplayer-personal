from aiogram import executor

from loader import dp
import handlers
from database.loader import load_db


async def on_startup(dp):
    await load_db()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
