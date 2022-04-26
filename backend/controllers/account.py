from fastapi import APIRouter, Depends, Body

from docs import docs
from models.models import User
from schemas.model_schemas import UserUpdate, UserOut, PasswordChange
from schemas.payloads import Tokens
from services.user_services import auth_service, user_service
from services.user_services.auth_service import authenticate
from services.util_service import raise_bad_request

router = APIRouter(
    prefix="/me",
    tags=["accounts"],
)


@router.get("", response_model=UserOut, responses=docs.get("me"))
async def get_account_data(user: User = Depends(authenticate)):
    return user


@router.put("", response_model=UserOut, responses=docs.get("edit_account_data"))
async def edit_account_data(user_data: UserUpdate, activation_url: str | None = Body(None),
                            user: User = Depends(authenticate)):
    result = await user_service.edit_account_data(user, user_data, activation_url)
    if not result.is_success:
        raise_bad_request(result.message)
    return result.value


@router.put("/password-change", response_model=Tokens, responses=docs.get("password_change"))
async def password_change(passwords: PasswordChange, user: User = Depends(authenticate)):
    result = await user_service.change_password(user, passwords)
    if not result.is_success:
        raise_bad_request(result.message)

    return auth_service.create_tokens(auth_service.create_token_data_for_user(result.value))
