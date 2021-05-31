from aiohttp import web

from loader import routes
from database import user

from loader import bot

from constants.config import BOT_TOKEN

from io import BytesIO


@routes.get('/user')
async def hello(request):
    return web.Response(text="user")


@routes.get('/user/photo')
async def info(request):
    user_id = request.query.get('user_id')

    if user_id is None:
        return web.HTTPBadRequest()

    photos_r = await bot.get_user_profile_photos(
        user_id=user_id
    )

    bf = BytesIO()

    await photos_r.photos[0][-1].download(destination=bf)

    return web.Response(body=bf, content_type="image/png")


@routes.get('/user/info')
async def info(request):
    user_id = request.query.get('user_id')
    chat_id = request.query.get('chat_id')

    if user_id is None or chat_id is None:
        return web.HTTPBadRequest()

    result = await bot.get_chat_member(
        user_id=user_id,
        chat_id=chat_id
    )

    res = {
        'first_name': result.user.first_name,
        'id': result.user.id,
        'last_name': result.user.last_name,
        'username': result.user.username
    }

    return web.json_response(res)


@routes.get('/user/activitytypes')
async def get_user_activities(request):
    chat_id = request.query.get('chat_id')

    if chat_id is None:
        return web.HTTPBadRequest()

    activities = await user.get_chat_activity_types(
        chat_id=int(chat_id)
    )

    results = list()

    for activity in activities:
        results.append({
            'id': activity.id,
            'name': activity.name
        })

    return web.json_response(results)


@routes.get('/user/subactivities')
async def get_user_subactivities(request):
    user_id = request.query.get('user_id')
    chat_id = request.query.get('chat_id')

    if user_id is None or chat_id is None:
        return web.HTTPBadRequest()

    subactivities = await user.get_all_user_subactivities(
        user_id=int(user_id),
        chat_id=int(chat_id)
    )

    results = list()

    for subactivity in subactivities:
        results.append({
            'id': subactivity.id,
            'name': subactivity.name,
            'activity_type_id': subactivity.activity_type
        })

    return web.json_response(results)
