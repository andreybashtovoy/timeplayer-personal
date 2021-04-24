from gino import Gino
from constants.config import POSTGRES_URI

db = Gino()


async def load_db():
    await db.set_bind(POSTGRES_URI)
    await db.gino.create_all()

