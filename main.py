from aiogram import executor
from aiohttp import web
import asyncio

from loader import dp
import handlers
from loader import routes
import api
import ssl

from database.loader import load_db
from constants import config
from aiohttp_middlewares import (
    cors_middleware
)

app = web.Application(middlewares=(
    [cors_middleware(allow_all=True)]
))

app.add_routes(routes)


async def on_startup(*args):
    await load_db()  # Подключение базы данных

    # Запуск API-сервера

    sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslcontext.load_cert_chain('certificate.crt', 'private.key')

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', config.API_PORT, ssl_context=sslcontext)
    await site.start()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
