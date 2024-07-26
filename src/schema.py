from datetime import datetime
from enum import Enum
from typing import List
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class FileCategory(Enum):
    IMAGE = 1
    DOCUMENT = 2
    VIDEO = 3
    AUDIO = 4
    ARCHIVE = 5
    MISC = 6

class Base(DeclarativeBase):
    pass

class File(Base):
    __tablename__ = 'file'

    id: Mapped[int] = mapped_column(primary_key=True)
    folder_id: Mapped[int] = mapped_column(ForeignKey('folder.id'))
    name: Mapped[str] = mapped_column(String(30))
    category: Mapped[FileCategory]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(default=None)

class Folder(Base):
    __tablename__ = 'folder'

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('folder.id'))
    parent: Mapped[List['Folder']] = relationship()
    files: Mapped[List['File']] = relationship()
    name: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(default=None)
