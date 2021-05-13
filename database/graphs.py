from .models import User, Chat, ChatXUser, ActivityType, Activity, ChatXActivityType, Subactivity
from sqlalchemy import and_, not_
from typing import Tuple
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import literal_column, text

from .loader import db


async def get_total_duration_with_benefit_by_days(user_id, chat_id, from_date, to_date):
    query = db.text(f"""
        WITH at AS(
            SELECT * FROM chats_x_activity_types
            WHERE chat_id={chat_id}
        ),
        t AS (
            SELECT a.*, DATE(start_time at time zone 'utc' at time zone 'Europe/Zaporozhye') as local_date
            FROM activities a
            INNER JOIN at on at.activity_type = a.activity_type
            WHERE at.with_benefit=TRUE AND user_id={user_id} AND at.chat_id={chat_id}
        )
        SELECT local_date, sum(duration) from t
        WHERE local_date BETWEEN '{from_date}' AND '{to_date}'
        GROUP BY local_date
    """)
    results = await db.all(query)

    return results


async def get_day_activities_data(user_id, chat_id, day):
    query = db.text(f"""
        SELECT a.*, at.name as activity_name, s.name as subactivity_name FROM activities a
        JOIN activity_types at on at.id = a.activity_type
        JOIN subactivities s on a.subactivity = s.id
        WHERE (start_time at time zone 'utc' at time zone 'Europe/Zaporozhye')::DATE = '{day}'
        AND a.user_id={user_id} AND a.chat_id={chat_id};
        """)
    results = await db.all(query)

    return results





