from enum import Enum

from pydantic import BaseModel

class FileCategory(Enum):
    IMAGE = 1
    DOCUMENT = 2
    VIDEO = 3
    AUDIO = 4
    ARCHIVE = 5
    MISC = 6

class File(BaseModel):
    name: str
    category: FileCategory

