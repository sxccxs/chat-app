from datetime import timedelta, datetime
from secrets import token_hex

import jwt
from asyncpg import DataError
from fastapi import Security, HTTPException, status, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from socketio.exceptions import ConnectionRefusedError
from jwt import PyJWTError
from pydantic import ValidationError

import config
from models.models import User
from results import VResult, Result
from schemas.payloads import Tokens, TokenData, ActivationPayload, UserTokenData, PasswordResetPayload
from services import util_service
from services.user_services import user_service, email_service, user_validation_service
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


def create_token_data_for_user(user: User) -> UserTokenData:
    return UserTokenData(
        id=user.id,
        hashed_password=user.hashed_password
    )


def create_tokens(user_data: UserTokenData) -> Tokens:
    return Tokens(
        access_token=create_access_token(user_data),
        refresh_token=create_refresh_token(user_data),
    )


def create_access_token(user_data: UserTokenData) -> str:
    return _create_token(user_data, ACCESS_TOKEN_TYPE, ACCESS_TOKEN_LIFETIME)


def create_refresh_token(user_data: UserTokenData) -> str:
    return _create_token(user_data, REFRESH_TOKEN_TYPE, REFRESH_TOKEN_LIFETIME)


def _create_token(user_data: UserTokenData, token_type: str, token_lifetime: timedelta) -> str:
    data_to_encode = TokenData(
        token_type=token_type,
        exp=datetime.utcnow() + token_lifetime,
        jti=_generate_jti(),
        **user_data.dict()
    )
    return jwt.encode(data_to_encode.dict(), config.SECRET_KEY, algorithm=ALGORITHM)


def _generate_jti() -> str:
    return str(int(datetime.utcnow().timestamp())) + token_hex(6)


def verify_token(token: str) -> VResult[TokenData]:
    try:
        data = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM], options={
            "verify_exp": True
        })
        token_data = TokenData(**data)
        return VResult(value=token_data)
    except (PyJWTError, ValidationError, ValueError, TypeError):
        return VResult(False, "Invalid token provided.")


def refresh_tokens(refresh_token: str) -> VResult[Tokens]:
    token_data_result = verify_token(refresh_token)
    if not token_data_result.is_success:
        return VResult[Tokens].from_result(token_data_result)

    if token_data_result.value.token_type != REFRESH_TOKEN_TYPE:
        return VResult[Tokens](False, "Invalid refresh token.")

    return VResult[Tokens](value=create_tokens(token_data_to_user_token_data(token_data_result.value)))


async def activate(payload: ActivationPayload) -> Result:
    try:
        uid = util_service.force_str(util_service.urlsafe_base64_decode(payload.uidb64))
        user = await User.objects.get_or_none(id=uid)
        if user and EMAIL_VERIFICATION_TOKEN_GENERATOR.check_token(user, payload.token):
            user.is_verified = True
            await user.save()
            return Result()
        return Result(False, "Invalid uidb64 or token")
    except (TypeError, ValueError, OverflowError, DataError):
        return Result(False, "Invalid uidb64 or token")


async def request_reset_password(email: str, reset_url: str) -> Result:
    user_result = await user_service.get_user_by_email(email)

    if not user_result:
        return user_result

    email_result = await email_service.send_password_reset_email(reset_url, user_result.value)
    if not email_result.is_success:
        return email_result

    return Result()


async def reset_password(payload: PasswordResetPayload) -> Result:
    validation_result = user_validation_service.validate_password(payload.new_password)
    if not validation_result.is_success:
        return validation_result

    try:
        uid = util_service.force_str(util_service.urlsafe_base64_decode(payload.uidb64))
        user = await User.objects.get_or_none(id=uid)
        if user and EMAIL_VERIFICATION_TOKEN_GENERATOR.check_token(user, payload.token):
            user_service.set_user_password(payload.new_password, user)
            await user.save()

            return Result()
        return Result(False, "Invalid uidb64 or token")
    except (TypeError, ValueError, OverflowError):
        return Result(False, "Invalid uidb64 or token")


async def authenticate(auth: HTTPAuthorizationCredentials = Security(BEARER)) -> User:
    user_result = await __authenticate(auth.credentials)
    if not user_result.is_success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=user_result.message)

    return user_result.value


async def authenticate_socket(auth: dict[str, str]) -> User:
    token = auth.get('token')
    user_result = await __authenticate(token)
    if not user_result.is_success:
        raise ConnectionRefusedError(user_result.message)

    return user_result.value


async def __authenticate(token: str) -> VResult[User]:
    invalid_result = VResult(False, "Invalid Token")
    token_result = verify_token(token)
    if not token_result.is_success or token_result.value.token_type != ACCESS_TOKEN_TYPE:
        return invalid_result
    user = await User.objects.get_or_none(id=token_result.value.id)
    if not user:
        return invalid_result
    if user.hashed_password != token_result.value.hashed_password:
        return invalid_result

    return VResult(value=user)


def set_refresh_token_cookie(response: Response, token: str) -> None:
    response.set_cookie(REFRESH_TOKEN_COOKIE_KEY, token,
                        max_age=int(REFRESH_TOKEN_LIFETIME.total_seconds()),
                        httponly=True, path="")


def token_data_to_user_token_data(token_data: TokenData) -> UserTokenData:
    return UserTokenData(
        id=token_data.id,
        hashed_password=token_data.hashed_password
    )
