from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, String, func, null
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.schemas import FileCategory

class Base(DeclarativeBase):
    pass

class File(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    category: Mapped[FileCategory]
    discord_id: Mapped[str] = mapped_column(String(24))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)

class Folder(Base):
    __tablename__ = 'folders'

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('folders.id'))
    parent: Mapped[List['Folder']] = relationship()
    name: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(default=None)
