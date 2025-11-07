from sqlmodel import create_engine, Session, select
from sqlalchemy import and_
from .db_models import Receipt, ReceiptStatus, SQLModel
from pathlib import Path
from typing import List

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DB_FILE = DATA_DIR / "receipts.db"
engine = create_engine(f"sqlite:///{DB_FILE}")


def init_db():
    SQLModel.metadata.create_all(engine)


def add_receipt(filename: str, filepath: str, uid: str) -> str:
    with Session(engine) as session:
        receipt = Receipt(filename=filename, filepath=filepath, uid=uid)
        session.add(receipt)
        session.commit()
        session.refresh(receipt)
        return receipt.id


def set_receipt_status(
    receipt_id: str,
    uid: str,
    status: ReceiptStatus,
) -> bool:
    with Session(engine) as session:
        statement = select(Receipt).where(
            and_(Receipt.id == receipt_id, Receipt.uid == uid)
        )
        receipt = session.exec(statement).first()

        if not receipt:
            return False

        receipt.status = status
        session.commit()
        return True


def get_receipts_by_status(uid: str, status: ReceiptStatus) -> List[Receipt]:
    with Session(engine) as session:
        statement = select(Receipt).where(
            and_(Receipt.status == status, Receipt.uid == uid)
        )

        receipts = session.exec(statement).all()
        return list(receipts)
