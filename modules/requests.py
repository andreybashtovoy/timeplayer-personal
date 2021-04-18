import aiohttp
import asyncio

from constants.config import BASE_URL


async def _make_request(url):
    """
    Base function for API requests
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                result = await resp.json()

                if result['status'] == 'success':
                    return result['data']
                else:
                    raise Exception
            else:
                raise Exception


async def get_user_activities(user_id) -> list:
    """
    :param user_id:
    :return: List of user's accessible activities
    """
    return await _make_request(f"{BASE_URL}/{user_id}/activitynames")