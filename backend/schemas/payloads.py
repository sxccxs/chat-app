from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

import enums
from models.models import User
from services.user_services.token_generator import TokenGenerator


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class RefreshPayload(BaseModel):
    refresh_token: str


class VerifyPayload(BaseModel):
    token: str


class UserTokenData(BaseModel):
    id: int
    hashed_password: str


class TokenData(BaseModel):
    id: int
    hashed_password: str
    token_type: str | None
    exp: datetime | None
    jti: str | None


@dataclass
class EmailPayload:
    url_prefix: str
    subject: str
    template_path: str
    user: User
    token_generator: TokenGenerator


class ActivationPayload(BaseModel):
    uidb64: str
    token: str


class PasswordResetPayload(ActivationPayload):
    new_password: str


class UserChatPayload(BaseModel):
    user_email: str
    chat_id: int


class ChangeRolePayload(BaseModel):
    user_email: str
    chat_id: int
    new_role_type: enums.RoleType
