from aiohttp import web
import aiofiles
import hmac
import hashlib
import binascii
import jwt

from constants import config
from loader import routes


@routes.get('/calendar/{user_id}/{chat_id}')
@routes.get('/user/{user_id}/{chat_id}')
async def get_index(request):
    async with aiofiles.open("dashboard/src/index.html", mode='r') as f:
        contents = await f.read()

    return web.Response(text=contents,
                        content_type='text/html')

routes.static("/", "dashboard/src/")



