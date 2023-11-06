import pandas as pd
from fastapi import Depends
from sqlalchemy.orm import Session

import app.models as models
from app.utils.dataframe_processor import DataframeProcessor
from app.utils.model_utils.file_model_utils import FileModelUtils


class ExcelFileManipulator:

    @staticmethod
    def preprocess_pandas_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        renaming_index = {df.columns[0]: "Код", df.columns[1]: "Наименование проекта"}
        for i in range(2, len(df.columns), 2):
            renaming_index[df.columns[i]] = str(df.columns[i]) + "_plan"
            renaming_index[df.columns[i + 1]] = str(df.columns[i]) + "_fact"
        result = df.rename(columns=renaming_index).tail(-1)
        return result

    @staticmethod
    def load_values_into_db(df: pd.DataFrame, filename: str, db: Session):
        preprocessed_dataframe = ExcelFileManipulator.preprocess_pandas_dataframe(df)
        file = FileModelUtils.db_create_new_file(db,filename)
        DataframeProcessor.process_dataframe(db,preprocessed_dataframe,file)

