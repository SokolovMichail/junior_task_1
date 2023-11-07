from __future__ import annotations

from typing import List, Tuple, Type

from sqlalchemy.orm import Session

from app import models
from app.models import File


class FileModelUtils:

    @staticmethod
    def get_file_version(db:Session,filename:str) -> int:
        version = 1
        previous_file = db.query(models.File) \
            .filter(models.File.file_name == filename) \
            .order_by(models.File.version.desc()) \
            .first()
        if previous_file is not None:
            version = previous_file.version + 1
        return version

    @staticmethod
    def db_create_new_file(db:Session, filename:str) -> File:
        version = FileModelUtils.get_file_version(db,filename)
        new_file = models.File(
            file_name=filename,
            version=version
        )
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
        return new_file

    @staticmethod
    def get_all_projects_from_file(db:Session,
                                  filename:str,
                                  version: int)\
        -> List[models.Fact] | List[models.Plan]:
        result = db.query(models.Project)\
            .join(models.File, models.File.id==models.Project.file_id)\
            .filter(models.File.file_name==filename,
                            models.File.version==version)\
            .all()
        return result


