from typing import Optional
from pydantic import BaseModel

class RequestAdd(BaseModel):
    fio: str
    topic: str
    num: str
    director: str
    user_id: int #could be telegram or discord id, or smth like that. maybe we can use login. but is field should be UNIQUE


class UserID(BaseModel):
    ok: bool = True
    user_id: int