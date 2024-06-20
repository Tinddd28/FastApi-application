from fastapi import APIRouter, Depends, File, UploadFile
from typing import Annotated
from src.models.user import UserAdd, UserID 
from src.googlesheets import User
from src.googledrive import File_cl

router = APIRouter(
    prefix="/methods",
    tags=["Методы"],
)


@router.post("/post")
async def add_user(user: Annotated[UserAdd, Depends()]) -> UserID:
    user_id = await User.add_user(user)
    return {"Ok": True, "user_id": user_id}


@router.get("/get")
async def  get_requests(id) -> list:
    return await User.get_requests(id)
    

@router.put("/file")
async def load_file(file: UploadFile = File(...)):
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return File_cl.load_file(file_location)


    