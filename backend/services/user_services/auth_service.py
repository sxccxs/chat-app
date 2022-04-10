from datetime import timedelta, datetime
from secrets import token_hex

import jwt
from fastapi import Security, HTTPException, status, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError
from sqlalchemy.orm import Session

import config
from models.db import session_maker
from models.models import User
from results import VResult, Result
from schemas.payloads import Tokens, TokenData, ActivationPayload
from services import util_service
from services.user_services import user_service
from services.user_services.email_service import EMAIL_VERIFICATION_TOKEN_GENERATOR

ACCESS_TOKEN_LIFETIME: timedelta = util_service.get_jwt_config_if_exists(
    "ACCESS_TOKEN_LIFETIME"
) or timedelta(minutes=30)

REFRESH_TOKEN_LIFETIME: timedelta = util_service.get_jwt_config_if_exists(
    "REFRESH_TOKEN_LIFETIME"
) or timedelta(hours=12)

ALGORITHM = util_service.get_jwt_config_if_exists("ALGORITHM") or "HS256"

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

REFRESH_TOKEN_COOKIE_KEY = "refresh_token"

BEARER = HTTPBearer()


def create_tokens(id: int) -> Tokens:
    return Tokens(
        access_token=create_access_token(id),
        refresh_token=create_refresh_token(id),
    )


def create_access_token(id: int) -> str:
    return _create_token(id, ACCESS_TOKEN_TYPE, ACCESS_TOKEN_LIFETIME)


def create_refresh_token(id: int) -> str:
    return _create_token(id, REFRESH_TOKEN_TYPE, REFRESH_TOKEN_LIFETIME)


def _create_token(id: int, token_type: str, token_lifetime: timedelta) -> str:
    data_to_encode = TokenData(
        id=id,
        token_type=token_type,
        exp=datetime.utcnow() + token_lifetime,
        jti=_generate_jti()
    )
    return jwt.encode(data_to_encode.dict(), config.SECRET_KEY, algorithm=ALGORITHM)


def _generate_jti() -> str:
    return str(int(datetime.utcnow().timestamp())) + token_hex(6)


def verify_token(token: str) -> VResult[TokenData]:
    try:
        data = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM], verify_exp=True)
        token_data = TokenData(**data)
        return VResult(value=token_data)
    except PyJWTError:
        return VResult(False, "Invalid token provided.")


def refresh_tokens(refresh_token: str) -> VResult[Tokens]:
    token_data_result = verify_token(refresh_token)
    if not token_data_result.is_success:
        return VResult[Tokens].from_result(token_data_result)

    if token_data_result.value.token_type != REFRESH_TOKEN_TYPE:
        return VResult[Tokens](False, "Invalid refresh token.")

    return VResult[Tokens](value=create_tokens(token_data_result.value.id))


def activate(db: Session, payload: ActivationPayload) -> Result:
    try:
        uid = util_service.force_str(util_service.urlsafe_base64_decode(payload.uidb64))
        user = db.get(User, uid)
        if user and EMAIL_VERIFICATION_TOKEN_GENERATOR.check_token(user, payload.token):
            user.is_active = True
            db.commit()
            return Result()
        return Result(False, "Invalid uidb64 or token")
    except (TypeError, ValueError, OverflowError):
        return Result(False, "Invalid uidb64 or token")


def authenticate(auth: HTTPAuthorizationCredentials = Security(BEARER)) -> User:
    token_result = verify_token(auth.credentials)
    if not token_result.is_success or token_result.value.token_type != ACCESS_TOKEN_TYPE:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=token_result.message)
    with session_maker() as session:
        user_result = user_service.get_active_user_by_id(session, token_result.value.id)
    if not user_result.is_success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=user_result.message)

    return user_result.value


def set_refresh_token_cookie(response: Response, token: str) -> None:
    response.set_cookie(REFRESH_TOKEN_COOKIE_KEY, token,
                        max_age=int(REFRESH_TOKEN_LIFETIME.total_seconds()),
                        httponly=True, path="")
