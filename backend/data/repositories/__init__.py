# repositories/__init__.py

from datetime import datetime
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_

from ..db_models import DbReceipt, DbReceiptItem, DbReceiptMetadata, ReceiptItemCategory
from .base_repository import BaseRepository
