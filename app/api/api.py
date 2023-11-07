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
    excel_df = pandas.read_excel(BytesIO(file.file.read()), sheet_name="data", header=0)
    file = ExcelFileManipulator().load_values_into_db(excel_df, file.filename, db)
    return {"data": f"File inserted under filename {file.file_name} , version {file.version}"}


@router.get("/api/file", status_code=200)
async def download_file(payload: FileModel,db: Session = Depends(get_db)):  # Ensures the input is greater than 0
    binary_excel_file = ExcelFileManipulator.return_file_from_db(db, payload)
    binary_excel_file.seek(0)
    return StreamingResponse(
        binary_excel_file,
        media_type="application/vnd.ms-excel",
        headers={"Content-Disposition": f"attachment; filename={payload.filename}"})
#
# @router.get("/api/diagram", status_code=200)
# async def update_blog(payload: Schema, id: int = Path(..., gt=0)):  # Ensures the input is greater than 0
#     note = await blog.get(id)
#     if not note:
#         raise HTTPException(status_code=404, detail="Note not found")
#     note_id = await blog.put(id, payload)
#     response_object = {
#         "id": note_id,
#         "title": payload.title,
#         "description": payload.description
#     }
#     return response_object
