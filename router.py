from fastapi import APIRouter, Depends
from typing import Annotated
from models.user import UserAdd, UserID 
from googlesheets import User


router = APIRouter()


@router.post("/post", tags=")))")
async def add_user(user: Annotated[UserAdd, Depends()]) -> UserID:
    user_id = await User.add_user(user)
    
    return {"Ok": True, "user_id": user_id}


@router.get("/get", tags="(")
async def  get_requests(id) -> list:
    return await User.get_requests(id)