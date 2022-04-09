from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class __UserBase(BaseModel):
    username: str
    email: str


class UserOut(__UserBase):
    class Config:
        orm_mode = True


class UserCreate(__UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    id: int
    username: str | None
    email: str | None
    is_active: bool | None
    password: str | None


class User(__UserBase):
    id: int
    is_active: bool
    chats: list[Chat] = []
    roles: list[Role] = []

    class Config:
        orm_mode = True


class _ChatBase(BaseModel):
    name: str


class ChatOut(_ChatBase):
    id: int

    class Config:
        orm_mode = True


class Chat(_ChatBase):
    id: int
    messages: list[Message] = []
    users: list[User] = []
    roles: list[Role] = []

    class Config:
        orm_mode = True


class __MessageBase(BaseModel):
    text: str


class MessageCreate(BaseModel):
    ...


class Message(BaseModel):
    id: int
    sending_time: datetime
    author_id: int
    chat_id: int

    class Config:
        orm_mode = True


class RoleType(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Role(BaseModel):
    id: int
    role_type: RoleType
    user: User
    chat: Chat

    class Config:
        orm_mode = True

