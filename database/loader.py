from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Base

from loader import dp

db_string = "postgresql+asyncpg://postgres:kpi@localhost:5432/time_player"

db = create_async_engine(db_string)

async_session = sessionmaker(
    db, expire_on_commit=False, class_=AsyncSession
)


async def load_db():
    async with db.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

