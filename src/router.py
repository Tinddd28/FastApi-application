from fastapi import APIRouter, Depends, File, UploadFile
from typing import Annotated
from src.models.request import RequestAdd, UserID
from src.googlesheets import google_sheets
from src.googledrive import File_cl

router = APIRouter(
    prefix="/methods",
    tags=["Методы"],
)


@router.post("/post")
async def add_user(request: Annotated[RequestAdd, Depends()]) -> UserID:
    user_id = await google_sheets.add_user(request)
    return {"Ok": True, "user_id": user_id}


@router.get("/get")
async def  get_requests(id) -> list:
    return await google_sheets.get_requests(id)
    

@router.put("/file")
async def load_file(request_id: int, file: UploadFile = File(...)):
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    file_dict = File_cl.load_file(file_location)
    res_update = await google_sheets.add_link(request_id, file_dict["file_url"])

    return {"ok": True, "request_id": request_id, "file_url": file_dict["file_url"]}


    