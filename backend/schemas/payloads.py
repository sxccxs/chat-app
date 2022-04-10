from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

from models.models import User
from services.user_services.token_generator import TokenGenerator


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class RefreshPayload(BaseModel):
    refresh_token: str


class VerifyPayload(BaseModel):
    token: str


class TokenData(BaseModel):
    id: int
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


class CheckEmailIn(BaseModel):
    email: str

