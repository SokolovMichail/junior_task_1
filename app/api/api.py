from __future__ import annotations

from io import BytesIO

import pandas
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse, JSONResponse

from app.database import get_db
from app.schemes.diagram_request import DiagramDataRequest
from app.schemes.diagram_response import DiagramDataResponse
from app.schemes.file_scheme import FileModel
from app.schemes.utils import Message
from app.utils.excel_file_manipulator import ExcelFileManipulator
from app.utils.model_utils.file_model_utils import FileModelUtils

router = APIRouter()


@router.post("/api/file", status_code=200)
async def upload_file(
        file: UploadFile,
        db: Session = Depends(get_db)
):
    """
    Загрузить файл в сервис

    """
    excel_df = pandas.read_excel(BytesIO(file.file.read()), sheet_name="data", header=0)
    file = ExcelFileManipulator().load_values_into_db(excel_df, file.filename, db)
    return {"data": f"File inserted under filename {file.file_name} , version {file.version}"}


@router.get("/api/file", response_model=None,
            responses={
                404: {"model": Message, "description": "The item was not found"},
                200: {
                    "content": {
                        "application/vnd.ms-excel": "file"
                    },
                },
            },
            )
async def download_file(file: FileModel = Depends(), db: Session = Depends(get_db)):
    """
    Сгенерировать и выгрузить excel файл на основе данных БД

    filename[str]: Имя файла, под которым он был загружен в БД

    version[int]: Версия файла

    """
    payload = FileModel(
        version=file.version,
        filename=file.filename
    )
    binary_excel_file = ExcelFileManipulator.return_file_from_db(db, payload)
    if binary_excel_file is None:
        return JSONResponse(status_code=404, content={"message": "The file you requested was not found"})
    binary_excel_file.seek(0)
    return StreamingResponse(
        binary_excel_file,
        media_type="application/vnd.ms-excel",
        headers={"Content-Disposition": f"attachment; filename={payload.filename}"})


@router.get("/api/year_report", response_model=DiagramDataResponse)
async def get_report(
        data: DiagramDataRequest = Depends(),
        db: Session = Depends(get_db)
) -> DiagramDataResponse:
    t = DiagramDataResponse(data=FileModelUtils.get_project_data_for_year(db, data),
                            year=data.year,
                            request_type=data.request_type)
    return t
