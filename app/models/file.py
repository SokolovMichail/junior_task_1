from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    version = Column(Integer)

