from __future__ import annotations

import copy
import math
from collections import defaultdict
from itertools import chain
from typing import Any, List
from datetime import datetime

import pandas as pd
from pandas import Series
from sqlalchemy.orm import Session

from app import models
from app.schemes.file_scheme import FileModel
from app.utils.model_utils.file_model_utils import FileModelUtils
from app.utils.model_utils.plan_fact_model_utils import PlanFactModelUtils
from app.utils.model_utils.project_model_utils import ProjectModelUtils


class DataframeProcessor:

    @staticmethod
    def process_dataframe(db: Session, df: pd.DataFrame, file: models.File):
        for row in df.iterrows():
            DataframeProcessor.process_dataframe_row(db, row[1], file)

    @staticmethod
    def process_dataframe_row(db: Session, row: Series, file: models.File):
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

    @staticmethod
    def append_plan_or_fact_to_dataframe(df: pd.DataFrame, project: models.Project, value: models.Fact | models.Plan):
        if project.project_id not in df['Код']:
            df.loc[len(df.index)] = {"Код": project.project_id, "Наименование проекта": project.name}
        data_str = value.date.strftime("%d.%m.%Y") + "_plan"
        df.loc[project.project_id]['data_str'] = value.value

    @staticmethod
    def construct_result_dataframe(requested_file: FileModel, db: Session):
        column_set = {"Код", "Наименование проекта"}
        dataframe_prepend_list = []
        projects = FileModelUtils.get_all_projects_from_file(db, requested_file.filename, requested_file.version)
        for project in projects:
            dataframe_prepend_list.append(DataframeProcessor.generate_product_row(db, project))
            column_set = column_set.union(set(dataframe_prepend_list[-1].keys()))
        column_dates = sorted(list(column_set.difference({"Код", "Наименование проекта"})))
        df_columns = ["Код", "Наименование проекта"] + DataframeProcessor.__generate_columns(column_dates)
        dataframe_prepend_list = [DataframeProcessor.flatten_prepend_dict(x) for x in dataframe_prepend_list]
        result_dataframe = pd.DataFrame.from_records(dataframe_prepend_list, columns=df_columns)
        return result_dataframe

    @staticmethod
    def generate_product_row(db: Session, project: models.Project):
        result = defaultdict(dict)
        result["Код"] = project.project_id
        result["Наименование проекта"] = project.name
        plans = ProjectModelUtils.get_plans_or_facts_for_project(db, project, models.Plan)
        facts = ProjectModelUtils.get_plans_or_facts_for_project(db, project, models.Fact)
        for plan in plans:
            result[plan.date]["план"] = plan.value
        for fact in facts:
            result[fact.date]["факт"] = fact.value
        return result

    @staticmethod
    def flatten_prepend_dict(row: defaultdict):
        skip_keys = ['Код', "Наименование проекта"]
        for element in set(row.keys()).difference(set(skip_keys)):
            for pf in ['план', 'факт']:
                if pf in row[element]:
                    row[element.strftime("%d.%m.%Y") + f"_{pf}"] = row[element][pf]
            row.pop(element)
        return row

    @staticmethod
    def __generate_columns(sorted_dates: List[datetime]) -> List[str]:
        def generate_date_plan_fact_string(date: datetime, addendum: str):
            return date.strftime("%d.%m.%Y") + f"_{addendum}"

        columns = list(chain.from_iterable(
            (generate_date_plan_fact_string(x, "план"),
             generate_date_plan_fact_string(x, "факт"))
            for x in sorted_dates))
        return columns
