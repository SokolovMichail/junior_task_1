from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    # Operating under the assumption that multiple files can contain identical projects.

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer)
    file_id = Column(Integer, ForeignKey("files.id"))
    name = Column(String)