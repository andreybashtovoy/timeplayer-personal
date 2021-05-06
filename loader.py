from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiohttp import web

from constants import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage()
dp = Dispatcher(bot, storage=storage)

routes = web.RouteTableDef()
