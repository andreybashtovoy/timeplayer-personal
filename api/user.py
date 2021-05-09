from aiohttp import web

from loader import routes
from database import user


@routes.get('/user')
async def hello(request):
    return web.Response(text="user")


@routes.get('/user/activitytypes')
async def get_user_activities(request):
    chat_id = request.query.get('chat_id')

    if chat_id is None:
        return web.json_response({
            'status': 'error',
            'message': 'chat_id is required'
        })

    activities = await user.get_chat_activity_types(
        chat_id=int(chat_id)
    )

    results = list()

    for activity in activities:
        results.append({
            'id': activity.id,
            'name': activity.name
        })

    return web.json_response({
        'status': 'ok',
        'data': results
    })


@routes.get('/user/subactivities')
async def get_user_subactivities(request):
    user_id = request.query.get('user_id')
    chat_id = request.query.get('chat_id')

    if user_id is None or chat_id is None:
        return web.json_response({
            'status': 'error',
            'message': 'user_id and chat_id are required'
        })

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

    return web.json_response({
        'status': 'ok',
        'data': results
    })
