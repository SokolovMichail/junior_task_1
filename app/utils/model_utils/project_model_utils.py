from sqlalchemy.orm import Session

from app import models
from app.models import File


class ProjectModelUtils:

    @staticmethod
    def insert_project_if_required(db:Session, file:File, project_id: int, project_name: str):
        project = db.query(models.Project)\
                .filter(models.Project.project_id == project_id)\
                .filter(models.Project.file_id == file.id) \
                .first()
        if project is None:
            project = models.Project(
                project_id=project_id,
                file_id = file.id,
                name=project_name,
            )
            db.add(project)
            db.commit()
            db.refresh(project)
        return project