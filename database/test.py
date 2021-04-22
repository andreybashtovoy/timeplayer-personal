from sqlalchemy.orm.session import Session

from .loader import async_session
from .models import A


async def test():
    async with async_session() as session:
        session.add(A(
            id=23,
            data="asdaed"
        ))

        await session.commit()
