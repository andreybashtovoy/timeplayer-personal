from aiohttp import web
import hmac
import hashlib
import binascii
import jwt

from constants import config
from loader import routes


@routes.get('/calendar/{user_id}/{chat_id}')
@routes.get('/user/{user_id}/{chat_id}')
async def tewr(request):
    return web.Response(text=open("dashboard/src/index.html").read(),
                        content_type='text/html')

routes.static("/", "dashboard/src/")



