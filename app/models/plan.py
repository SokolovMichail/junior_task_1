from sqlalchemy import Column, Integer,ForeignKey, Float, Date

from app.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    internal_project_id = Column(Integer, ForeignKey("projects.id"))
    date = Column(Date)
    value = Column(Float)