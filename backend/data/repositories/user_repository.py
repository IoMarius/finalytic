from typing import Optional
from sqlmodel import Session, select
from ..db_models import DbUser
from .base_repository import BaseRepository


class UserRepository(BaseRepository[DbUser]):
    def __init__(self, session: Session):
        super().__init__(DbUser, session)

    def get_by_telegram_id(self, telegram_id: str) -> Optional[DbUser]:
        statement = select(DbUser).where(DbUser.telegram_uid == telegram_id)
        return self.session.exec(statement).first()

    def create_user(
        self,
        telegram_id: str,
        passphrase: Optional[str],  # TODO: optional passphrase for now :)
    ) -> DbUser:
        user = DbUser(telegram_uid=telegram_id, passphrase=passphrase)
        return self.create(user)

    def user_exists(self, telegram_id: str) -> bool:
        return self.get_by_telegram_id(telegram_id) is not None

    def verify_passphrase(self, telegram_id: str, passphrase: str) -> bool:
        user = self.get_by_telegram_id(telegram_id)
        if user:
            # TODO: password hashing (bcrypt, argon2)
            return user.passphrase == passphrase
        return False
