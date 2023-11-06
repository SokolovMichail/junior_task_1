from sqlalchemy import Column, Integer,ForeignKey, Float, Date

from app.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    project_id = Column(Integer, ForeignKey("project.id"))
    date = Column(Date)
    value = Column(Float)