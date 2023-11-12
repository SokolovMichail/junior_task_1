from typing import Dict

from pydantic import BaseModel

from app.schemes.diagram_request import TypeEnum


class DiagramDataResponse(BaseModel):
    year: int
    request_type: TypeEnum
    data: Dict[int, float]
