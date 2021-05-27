from aiogram import executor
from aiohttp import web
import asyncio

from loader import dp
import handlers
from loader import routes
import api

from database.loader import load_db
from constants import config
from aiohttp_middlewares import (
    cors_middleware
)
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS

app = web.Application(middlewares=(
    [cors_middleware(
        origins=["https://manage.sslforfree.com/", "http://timeplayer-new.loca.lt/", "http://timeplayer.loca.lt/"],
        #allow_all=True,
        allow_credentials=True,
        allow_methods=("POST", "PATCH"),
        allow_headers=DEFAULT_ALLOW_HEADERS
                      + ("X-Client-UID",),
    )]
))

app.add_routes(routes)


async def on_startup(*args):
    await load_db()  # Подключение базы данных

    # Запуск API-сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', config.API_PORT)
    await site.start()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
