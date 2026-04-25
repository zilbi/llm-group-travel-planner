import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession
from sqlalchemy import select
from typing import List

from db.model.history import History, Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)


class Database:
    def __init__(
        self,
    ):
        self.engine = engine
        self.async_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def create_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def history_add(self, chat_id: int, text: str):
        async with self.async_session() as session:
            async with session.begin():
                history = History(
                    chat_id=chat_id, text=text,
                )
                session.add(history)

            await session.commit()

    async def get_history(self, chat_id: int) -> List[History]:
        async with self.async_session() as session:
            result = await session.execute(
                select(History).where(History.chat_id == chat_id)
            )
            return result.scalars().all()

    async def get_session(self) -> AsyncSession:
        return self.async_session()

    async def close(self):
        await self.engine.dispose()
