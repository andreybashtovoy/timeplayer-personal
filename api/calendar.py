from aiohttp import web
from datetime import datetime
from dateutil import tz
import jwt

from constants import config
from loader import routes
from database import calendar


def is_valid_token(token, user_id) -> bool:
    try:
        decoded = jwt.decode(token, config.BOT_TOKEN, algorithms=["HS256"])
    except Exception as e:
        print(e)
        return False

    if decoded['id'] == user_id:
        return True
    return False


@routes.post('/calendar/activities')
async def get_activities(request):
    data = await request.post()

    from_date = datetime.fromtimestamp(int(data['from_date']) / 1000)
    to_date = datetime.fromtimestamp(int(data['to_date']) / 1000)

    if not is_valid_token(data['token'], data['user_id']):
        return web.json_response({
            'status': 'error',
            'message': 'token is invalid'
        })

    activities = await calendar.get_user_activities(
        user_id=int(data['user_id']),
        chat_id=int(data['chat_id']),
        from_date=from_date,
        to_date=to_date
    )

    results = list()

    to_tz = tz.gettz('Europe/Zaporozhye')

    for activity in activities:
        results.append({
            'id': activity.id,
            'activity_type': activity.activity_type,
            'subactivity': activity.subactivity,
            'start_time': activity.start_time.astimezone(to_tz).timestamp(),
            'end_time': activity.start_time.astimezone(to_tz).timestamp()
        })

    return web.json_response({
        'status': 'ok',
        'data': results
    })
