# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select

# from db.model.history import History


# class HistoryModel:
#     def __init__(self, session: AsyncSession):
#         self.session = session

#     async def history_add(self, chat_id: int, text: str) -> History:
#         history = History(chat_id=chat_id, text=text,)
#         self.session.add(history)
#         await self.session.commit()
#         return history


#     async def history_get(self, chat_id: int) -> list[History]:
#         result = await self.session.execute(
#             select(History).where(History.chat_id==chat_id).order_by(History.id)
#         )