from __future__ import annotations

import datetime

from pydantic import BaseModel


class __UserBase(BaseModel):
    username: str
    email: str


class UserOut(__UserBase):
    is_verified: bool

    class Config:
        orm_mode = True


class UserCreate(__UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    username: str | None
    email: str | None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class _ChatBase(BaseModel):
    name: str


class ChatCreate(_ChatBase):
    ...


class ChatEdit(_ChatBase):
    id: int


class ChatOut(_ChatBase):
    id: int

    class Config:
        orm_mode = True


class __MessageBase(BaseModel):
    text: str


class MessageCreate(__MessageBase):
    chat_id: int


class MessageOut(__MessageBase):
    id: int
    chat: ChatOut
    sending_time: datetime.datetime

    class Config:
        orm_mode = True
