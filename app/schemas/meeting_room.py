from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class MeetingRoomCreate(MeetingRoomBase):

    name: str = Field(..., min_length=1, max_length=100)


class MeetingRoomDB(MeetingRoomCreate):

    id: int

    class Config:

        orm_mode = True


class MeetigRoomUpdate(MeetingRoomBase):

    @validator('name')
    def name_cant_be_null(cls, value):
        if not value:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value
