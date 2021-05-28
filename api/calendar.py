from aiohttp import web
from datetime import datetime
from dateutil import tz
import jwt

from constants import config
from loader import routes
from database import calendar

local_tz = tz.gettz('Europe/Zaporozhye')


def is_valid_token(token, user_id) -> bool:

    print(token, user_id)

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
    data = await request.json()

    token = request.cookies.get('token')

    if not is_valid_token(token, data['user_id']):
        return web.HTTPUnauthorized()

    from_date = datetime.fromtimestamp(int(data['from_date']) / 1000, tz=local_tz)
    to_date = datetime.fromtimestamp(int(data['to_date']) / 1000, tz=local_tz)

    activities = await calendar.get_user_activities(
        user_id=int(data['user_id']),
        chat_id=int(data['chat_id']),
        from_date=from_date.astimezone(tz=tz.UTC).replace(tzinfo=None),
        to_date=to_date.astimezone(tz=tz.UTC).replace(tzinfo=None)
    )

    results = list()



    for activity in activities:
        print(type((activity.start_time.astimezone(local_tz) + activity.duration).timestamp()))

        results.append({
            'id': activity.id,
            'activity_type': activity.activity_type,
            'subactivity': activity.subactivity,
            'start_time': activity.start_time.astimezone(local_tz).timestamp(),
            'end_time1': (activity.start_time.astimezone(local_tz) + activity.duration).timestamp(),
            'activity_name': activity.activity_name,
            'subactivity_name': activity.subactivity_name
        })

    return web.json_response(results)


@routes.post('/calendar/add')
async def add_activity(request):
    data = await request.json()

    token = request.cookies.get('token')

    if not is_valid_token(token, data['user_id']):
        return web.HTTPUnauthorized()

    start_time = datetime.fromtimestamp(int(data['start_time']) / 1000, tz=local_tz).astimezone(tz.UTC).replace(tzinfo=None)
    end_time = datetime.fromtimestamp(int(data['end_time']) / 1000, tz=local_tz).astimezone(tz.UTC).replace(tzinfo=None)

    activity = await calendar.create_activity(
        user_id=int(data['user_id']),
        chat_id=int(data['chat_id']),
        start_time=start_time,
        duration=end_time - start_time,
        activity_type_id=data['activity_type_id'],
        subactivity_id=data['subactivity_id']
    )

    return web.json_response({
        'activity_id': activity.id
    })


@routes.post('/calendar/delete')
async def remove_activity(request):
    data = await request.json()

    token = request.cookies.get('token')

    if not is_valid_token(token, data['user_id']):
        return web.HTTPUnauthorized()

    await calendar.remove_activity(data['activity_id'])

    return web.HTTPOk()


@routes.post('/calendar/edit')
async def edit_activity(request):
    data = await request.json()

    token = request.cookies.get('token')

    if not is_valid_token(token, data['user_id']):
        return web.HTTPUnauthorized()

    start_time = datetime.fromtimestamp(int(data['start_time']) / 1000, tz=local_tz).astimezone(tz.UTC).timestamp()
    end_time = datetime.fromtimestamp(int(data['end_time']) / 1000, tz=local_tz).astimezone(tz.UTC).timestamp()

    await calendar.edit_activity(
        start_time=start_time,
        duration=end_time - start_time,
        activity_type_id=data['activity_type_id'],
        subactivity_id=data['subactivity_id'],
        activity_id=data['activity_id']
    )

    return web.HTTPOk()
