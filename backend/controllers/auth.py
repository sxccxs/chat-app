from fastapi import HTTPException, status, APIRouter, Body, Response, Request

from enums import EmailStatus
from models.db import session_maker
from schemas import payloads
from schemas.model_schemas import UserLogin, UserCreate
from services.user_services import auth_service, user_service, email_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=payloads.Tokens)
async def login(payload: UserLogin):
    with session_maker() as session:
        user_result = user_service.get_active_user_by_email(session, payload.email)
    if not user_result.is_success or not user_service.check_password(user_result.value, payload.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with given credentials was not found.")

    tokens = auth_service.create_tokens(user_result.value.id)

    return tokens


@router.post("/refresh", response_model=payloads.Tokens)
async def refresh(payload: payloads.RefreshPayload):
    result = auth_service.refresh_tokens(payload.refresh_token)
    if not result.is_success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=result.message)

    return result.value


@router.post("/verify", status_code=status.HTTP_204_NO_CONTENT)
async def verify(payload: payloads.VerifyPayload):
    result = auth_service.verify_token(payload.token)
    if not result.is_success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=result.message)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register(user: UserCreate, activation_url: str = Body(...)):
    with session_maker() as session:
        result = user_service.create_user(session, user)
    if not result.is_success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=result.message)
    result = email_service.send_activation_email(activation_url, result.value)
    if not result.is_success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=result.message)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate(payload: payloads.ActivationPayload):
    with session_maker() as session:
        result = auth_service.activate(session, payload)
    if not result.is_success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=result.message)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/check-email-exists", response_model=payloads.CheckEmailOut)
async def check_email_exists(payload: payloads.CheckEmailIn):
    with session_maker() as session:
        result = user_service.get_user_by_email(session, payload.email)
    if result.is_success:
        return payloads.CheckEmailOut(result=EmailStatus.EMAIL_EXISTS)
    return payloads.CheckEmailOut(result=EmailStatus.EMAIL_DOES_NOT_EXIST)
