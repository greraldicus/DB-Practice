from __future__ import annotations
from pydantic import BaseModel


class RegionsBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class PeopleBase(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    sex: str
    region_id: int = None

    class Config:
        orm_mode = True