import math
from typing import Any
from datetime import datetime

import pandas as pd
from pandas import Series
from sqlalchemy.orm import Session

from app import models
from app.utils.model_utils.plan_fact_model_utils import PlanFactModelUtils
from app.utils.model_utils.project_model_utils import ProjectModelUtils


class DataframeProcessor:

    @staticmethod
    def process_dataframe(db:Session,df:pd.DataFrame, file:models.File):
        for row in df.iterrows():
            DataframeProcessor.process_dataframe_row(db,row[1],file)


    @staticmethod
    def process_dataframe_row(db:Session, row:Series, file: models.File):
        project = ProjectModelUtils.insert_project_if_required(db,
                                                     file,
                                                     row['Код'],
                                                     row["Наименование проекта"])
        for index, value in row[2:].items():
            date_str, type_str = index.split("_")
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
            type_to_insert = models.Plan if type_str == "plan" else models.Fact
            if not math.isnan(value):
                PlanFactModelUtils.insert_data_info(db,
                                                    project,
                                                    date,
                                                    value,
                                                    type_to_insert
                                                    )


