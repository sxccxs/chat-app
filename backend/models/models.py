import datetime
from functools import partial

from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from models.db import Base

NotNullColumn = partial(Column, nullable=False)


class BaseModel:
    id = NotNullColumn(Integer, primary_key=True, index=True, autoincrement=True)


userChatTable = Table('users_chats', Base.metadata,
                      Column('user_id', ForeignKey('users.id'), primary_key=True),
                      Column('chat_id', ForeignKey('chats.id'), primary_key=True)
                      )


class User(Base, BaseModel):
    __tablename__ = "users"

    email = NotNullColumn(String, unique=True, index=True)
    username = NotNullColumn(String)
    hashed_password = NotNullColumn(String)
    is_active = NotNullColumn(Boolean, default=False)
    chats = relationship(
        "Chat",
        secondary=userChatTable,
        back_populates="users",
    )
    roles = relationship(
        "Role",
        back_populates="user",
    )


class Chat(Base, BaseModel):
    __tablename__ = "chats"

    name = NotNullColumn(String)
    users = relationship(
        "User",
        secondary=userChatTable,
        back_populates="chats",
    )
    roles = relationship(
        "Role",
        back_populates="chat",
    )
    messages = relationship(
        "Message",
        back_populates="chat",
    )


class Message(Base, BaseModel):
    __tablename__ = "messages"

    text = NotNullColumn(String)
    sending_time = NotNullColumn(DateTime, default=datetime.datetime.now)
    chat_id = NotNullColumn(Integer, ForeignKey("chats.id"))
    chat = relationship(
        "Chat",
        back_populates="messages",
    )
    author_id = NotNullColumn(Integer, ForeignKey("users.id"))
    author = relationship("User")


class RoleType(Base, BaseModel):
    __tablename__ = "role_types"

    name = NotNullColumn(String, unique=True, index=True)


class Role(Base, BaseModel):
    __tablename__ = "roles"

    role_type_id = NotNullColumn(Integer, ForeignKey("role_types.id"))
    role_type = relationship("RoleType", uselist=False)
    user_id = NotNullColumn(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="roles")
    chat_id = NotNullColumn(Integer, ForeignKey("chats.id"))
    chat = relationship("Chat", back_populates="roles")

    __table_arg__ = (UniqueConstraint("user_id", "chat_id"),)
