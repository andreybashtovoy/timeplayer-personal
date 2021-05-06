from aiohttp import web

from loader import routes


@routes.get('/user')
async def hello(request):
    return web.Response(text="user")
