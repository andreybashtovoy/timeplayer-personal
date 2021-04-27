from .models import Activity, ActivityType


async def start_activity(user_id, activity_type):
    activity = await Activity.create(
        user_id=user_id,
        activity_type=activity_type
    )

    print(activity)
