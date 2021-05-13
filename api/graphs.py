from aiohttp import web
from datetime import datetime
from dateutil import tz
import jwt

from constants import config
from loader import routes
from database import graphs

local_tz = tz.gettz('Europe/Zaporozhye')


@routes.post('/graphs/heatmap')
async def get_heatmap(request):
    data = await request.post()

    results = await graphs.get_total_duration_with_benefit_by_days(
        user_id=data['user_id'],
        chat_id=data['chat_id'],
        from_date=data['from_date'],
        to_date=data['to_date']
    )

    response = list()

    for obj in results:
        response.append({
            'day': obj.local_date.strftime("%Y-%m-%d"),
            'value': obj.sum.total_seconds()/60/60
        })

    return web.json_response(response)


@routes.post('/graphs/day-activities')
async def get_day_activities(request):
    data = await request.post()

    results = await graphs.get_day_activities_data(
        user_id=data['user_id'],
        chat_id=data['chat_id'],
        day=data['day']
    )

    response = list()

    response = []

    def add_activity(name):
        for i in range(len(response)):
            if response[i]['name'] == name:
                return i

        response.append({
            "name": name,
            "value": list()
        })

        return -1

    def add_project(name, value, index):
        obj_list = response[index]['value']

        for i in range(len(obj_list)):
            if obj_list[i]['project'] == name:
                obj_list[i]['value'] += value
                return

        obj_list.append({
            'project': name,
            'value': value
        })

    for activity in results:
        index = add_activity(activity.activity_name)

        add_project(
            name=activity.subactivity_name or "-",
            value=activity.duration.total_seconds()/60/60,
            index=index
        )

    return web.json_response(response)
