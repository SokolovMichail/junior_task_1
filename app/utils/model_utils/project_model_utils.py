from __future__ import annotations

from typing import Type, List

from sqlalchemy.orm import Session

from app import models


class ProjectModelUtils:

    @staticmethod
    def insert_project_if_required(db: Session, file: models.File, project_id: int, project_name: str):
        project = db.query(models.Project) \
            .filter(models.Project.project_id == project_id) \
            .filter(models.Project.file_id == file.id) \
            .first()
        if project is None:
            project = models.Project(
                project_id=project_id,
                file_id=file.id,
                name=project_name,
            )
            db.add(project)
            db.commit()
            db.refresh(project)
        return project

    @staticmethod
    def get_plans_or_facts_for_project(db: Session, project: models.Project,
                                       type_to_get: Type[models.Plan | models.Fact]) \
            -> List[models.Plan] | List[models.Fact]:
        return db.query(type_to_get).filter(type_to_get.internal_project_id == project.id).all()
