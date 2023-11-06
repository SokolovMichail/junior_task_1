from __future__ import annotations

from datetime import datetime
from typing import Type

from sqlalchemy.orm import Session

from app import models


class PlanFactModelUtils:

    @staticmethod
    def insert_data_info(db:Session,
                         project: models.Project,
                         datetime:datetime,
                         value: float,
                         to_insert: Type[models.Fact | models.Plan]):
        inserted = to_insert(
            internal_project_id = project.id,
            date = datetime,
            value = value,
        )
        db.add(inserted)
        db.commit()
        db.refresh(inserted)