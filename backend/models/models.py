from __future__ import annotations

import datetime
import ormar
import constants
from models.db import database, metadata


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class PrimaryKeyMixin:
    id: int = ormar.Integer(primary_key=True)


class User(ormar.Model, PrimaryKeyMixin):
    class Meta(MainMeta):
        ...

    email: str = ormar.String(max_length=constants.MAX_EMAIL_LENGTH, unique=True, index=True)
    is_verified: bool = ormar.Boolean(default=False)
    username: str = ormar.String(max_length=constants.MAX_USERNAME_LENGTH, min_length=constants.MIN_USERNAME_LENGTH,
                                 index=True)
    hashed_password: str = ormar.String(max_length=255)


class Chat(ormar.Model, PrimaryKeyMixin):
    class Meta(MainMeta):
        ...

    name: str = ormar.String(max_length=constants.MAX_CHATNAME_LENGTH, min_length=constants.MIN_CHATNAME_LENGTH,
                             index=True)
    users: list[User] | None = ormar.ManyToMany(to=User)


class Message(ormar.Model, PrimaryKeyMixin):
    class Meta(MainMeta):
        ...

    text: str = ormar.Text()
    sending_time: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    chat: Chat = ormar.ForeignKey(Chat, nullable=False)
    author: User = ormar.ForeignKey(User, nullable=False)


class RoleType(ormar.Model, PrimaryKeyMixin):
    class Meta(MainMeta):
        ...

    name = ormar.String(max_length=255, unique=True, index=True)


class Role(ormar.Model, PrimaryKeyMixin):
    class Meta(MainMeta):
        constraints = [ormar.UniqueColumns("user", "chat")]

    role_type: RoleType = ormar.ForeignKey(RoleType, nullable=False)
    user: User = ormar.ForeignKey(User, nullable=False)
    chat: Chat = ormar.ForeignKey(Chat, nullable=False)