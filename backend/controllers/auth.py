import logging

from fastapi import status, APIRouter, Body, Response, HTTPException

from docs import docs
from models.models import User
from schemas import payloads
from schemas.model_schemas import UserLogin, UserCreate
from schemas.payloads import PasswordResetPayload
from services.user_services import auth_service, user_service
from services.util_service import raise_bad_request

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=payloads.Tokens, responses=docs.get("login"))
async def login(payload: UserLogin):
    user = await User.objects.get_or_none(email=payload.email)
    if not user or not user_service.is_password_correct(user, payload.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with given credentials was not found.")

    tokens = auth_service.create_tokens(auth_service.create_token_data_for_user(user))

    return tokens


@router.post("/refresh", response_model=payloads.Tokens, responses=docs.get("refresh"))
async def refresh(payload: payloads.RefreshPayload):
    result = auth_service.refresh_tokens(payload.refresh_token)
    if not result.is_success:
        raise_bad_request(result.message)

    return result.value


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT, responses=docs.get("register"))
async def register(user: UserCreate, activation_url: str = Body(...)):
    result = await user_service.register(user, activation_url)
    if not result.is_success:
        raise_bad_request(result.message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/activate", status_code=status.HTTP_204_NO_CONTENT, responses=docs.get("activate"))
async def activate(payload: payloads.ActivationPayload):
    result = await auth_service.activate(payload)
    if not result.is_success:
        raise_bad_request(result.message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/check-email-exists", responses=docs.get("check_email_exists"))
async def check_email_exists(email: str = Body(..., embed=True)):
    user = await User.objects.get_or_none(email=email)
    if user:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(email: str = Body(..., embed=True), reset_url: str = Body(..., embed=True)):
    result = await auth_service.request_reset_password(email, reset_url)
    if not result.is_success:
        raise_bad_request(result.message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/reset-password-confirm", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password_confirm(payload: PasswordResetPayload):
    result = await auth_service.reset_password(payload)
    if not result.is_success:
        raise_bad_request(result.message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
