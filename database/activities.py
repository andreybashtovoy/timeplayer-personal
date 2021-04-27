from .models import Activity, ActivityType
from .user import get_user_accessible_activity_types


async def start_activity_by_name(user_id, activity_name) -> Activity:
    activity_types = await get_user_accessible_activity_types(user_id)

    activity_type_id = None

    for activity_type in activity_types:
        if activity_type.name == activity_name:
            activity_type_id = activity_type.id
            break

    if activity_type_id is not None:
        activity = await start_activity(user_id, activity_type_id)
        return activity


async def start_activity(user_id, activity_type) -> Activity:
    activity = await Activity.create(
        user_id=user_id,
        activity_type=activity_type
    )

    return activity
