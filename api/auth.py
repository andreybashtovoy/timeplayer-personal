from aiohttp import web
import hmac
import hashlib
import jwt

from constants import config
from loader import routes


@routes.get('/')
async def tewr(request):
    return web.Response(text="""
    <script async src="https://telegram.org/js/telegram-widget.js?14" data-telegram-login="timeplayer_sdbot" data-size="large" data-onauth="onTelegramAuth(user)" data-request-access="write"></script>
    <script type="text/javascript">
      function onTelegramAuth(user) {
        alert('Logged in as ' + user.first_name + ' ' + user.last_name + ' (' + user.id + (user.username ? ', @' + user.username : '') + ')');
      }
    </script>
    """,
                        content_type='text/html')


@routes.get('/auth')
async def hello(request):
    data = await request.post()

    data_hash = data.pop('hash')

    data_check_list = list()

    for key in data:
        data_check_list.append(
            f"{key}={data[key]}"
        )

    data_check_string = "\n".join(data_check_list)

    signature = hmac.new(config.BOT_TOKEN, data_check_string, hashlib.sha256).hexdigest()

    if signature == data_hash:
        encoded = jwt.encode(data, config.BOT_TOKEN, algorithm="HS256")

        resp = {
            "status": "ok",
            "token": encoded
        }
    else:
        resp = {
            "status": "error"
        }

    return web.json_response(resp)
