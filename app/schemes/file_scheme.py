from pydantic import BaseModel

class FileModel(BaseModel):
    version:int
    filename:str