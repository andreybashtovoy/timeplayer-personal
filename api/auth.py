from aiohttp import web
import hmac
import hashlib
import binascii
import jwt

from constants import config
from loader import routes


@routes.get('/')
async def tewr(request):
    return web.Response(text=open("api/test.html").read(),
                        content_type='text/html')


@routes.post('/auth')
async def hello(request):
    data = await request.post()

    data = dict(data)

    print(data)

    data_hash = data.pop('hash')

    data = dict(sorted(data.items(), key=lambda x: x[0].lower()))

    data_check_list = list()

    for key in data:
        data_check_list.append(
            f"{key}={data[key]}"
        )

    data_check_string = "\n".join(data_check_list)

    secret_key = hashlib.sha256(config.BOT_TOKEN.encode()).digest()
    _hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    if _hash == data_hash:
        encoded = jwt.encode(data, config.BOT_TOKEN, algorithm="HS256")

        response = web.HTTPOk()

        response.set_cookie(
            name="token",
            value=encoded,
            max_age=60*60*24*30,
            httponly=True
        )

        return response
    else:
        return web.HTTPBadRequest()


@routes.post('/get_user')
async def get_user(request):
    data = await request.post()

    try:
        token = request.cookies.get('token')

        decoded = jwt.decode(token, config.BOT_TOKEN, algorithms=["HS256"])

        if decoded['id'] == data['user_id']:
            return web.json_response(decoded)
    except Exception as e:
        return web.HTTPUnauthorized()


@routes.get('/.well-known/pki-validation/577AFFC229945C574E2A6A846FC188B8.txt')
async def pki(request):
    return web.Response(text="""72C73D1B6E009F50629C3D61B37EC22A28406BB2F42B1229CE1B29E4A3210D99
comodoca.com
2ab628acd8d3f15""",
                        content_type='text/html')