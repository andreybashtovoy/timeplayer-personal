from aiogram import executor
from aiohttp import web
import asyncio

from loader import dp
import handlers
from loader import routes
import api

from database.loader import load_db
from constants import config

app = web.Application()

app.add_routes(routes)


async def on_startup(*args):
    await load_db()  # Подключение базы данных.loca.lt/

    # Запуск API-сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', config.API_PORT)
    await site.start()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
