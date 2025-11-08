from typing import Optional
from sqlmodel import select
from ..db_models import DbUser
from .base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[DbUser]):

    def __init__(self, session: AsyncSession):
        super().__init__(DbUser, session)

    async def get_by_telegram_id(self, telegram_id: str) -> Optional[DbUser]:
        statement = select(DbUser).where(DbUser.telegram_uid == telegram_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_user(
        self, telegram_id: str, passphrase: Optional[str] = None
    ) -> DbUser:
        user = DbUser(telegram_uid=telegram_id, passphrase=passphrase)
        return await self.create(user)

    async def user_exists(self, telegram_id: str) -> bool:
        return await self.get_by_telegram_id(telegram_id) is not None

    async def verify_passphrase(self, telegram_id: str, passphrase: str) -> bool:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            # TODO: password hashing
            return user.passphrase == passphrase
        return False
