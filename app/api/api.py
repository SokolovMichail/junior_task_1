from io import BytesIO

import pandas
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.database import get_db
from app.schemes.file_scheme import FileModel
from app.utils.excel_file_manipulator import ExcelFileManipulator

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


@router.get("/api/file/{filename}_{version}",response_model=None,response_class=StreamingResponse)
async def download_file(filename:str, version: str, db: Session = Depends(get_db)) -> StreamingResponse:
    """
    Сгенерировать и выгрузить excel файл на основе данных БД

    filename[str]: Имя файла, под которым он был загружен в БД

    version[int]: Версия файла

    """
    # Изначально я хотел payload поместить в download file.
    # Но это портит SwaggerUI( нельзя выполнить данный запрос)
    # Поэтому пришлось вот так.
    payload = FileModel(
        version=version,
        filename=filename
    )
    binary_excel_file = ExcelFileManipulator.return_file_from_db(db,payload)
    binary_excel_file.seek(0)
    return StreamingResponse(
        binary_excel_file,
        media_type="application/vnd.ms-excel",
        headers={"Content-Disposition": f"attachment; filename={payload.filename}"})
