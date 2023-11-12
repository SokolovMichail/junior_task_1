from enum import Enum

from app.schemes.file_scheme import FileModel


class TypeEnum(str, Enum):
    plan = 'plan'
    fact = 'fact'


class DiagramDataRequest(FileModel):
    year: int
    request_type: TypeEnum
