from fastapi import APIRouter, Depends, Response, status, Body

from models.models import User
from schemas.model_schemas import ChatOut, ChatCreate, ChatEdit, UserOut
from schemas.payloads import UserChatPayload, ChangeRolePayload
from services.chat_services import chat_service
from services.user_services.auth_service import authenticate
from services.util_service import raise_bad_request

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)


@router.get("", response_model=list[ChatOut])
async def get_chats(user: User = Depends(authenticate)):
    return await chat_service.get_user_chats(user)


@router.post("", response_model=ChatOut)
async def create_chat(chat_data: ChatCreate, user: User = Depends(authenticate)):
    result = await chat_service.create_chat_by_user(chat_data, user)
    if not result.is_success:
        raise_bad_request(result.message)

    return result.value


@router.put("", response_model=ChatOut)
async def edit_chat(chat_data: ChatEdit, user: User = Depends(authenticate)):
    result = await chat_service.edit_chat_by_user(chat_data, user)
    if not result.is_success:
        raise_bad_request(result.message)

    return result.value


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: int = Body(..., embed=True), user: User = Depends(authenticate)):
    result = await chat_service.delete_chat_by_user(chat_id, user)
    if not result.is_success:
        raise_bad_request(result.message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/users/{chat_id}", response_model=list[UserOut])
async def get_chat_users(chat_id: int, user: User = Depends(authenticate)):
    result = await chat_service.get_chat_users(chat_id, user)
    if not result.is_success:
        raise_bad_request(result.message)
    return result.value


@router.post("/users", status_code=status.HTTP_204_NO_CONTENT)
async def add_user_to_chat(payload: UserChatPayload, user: User = Depends(authenticate)):
    result = await chat_service.add_user_to_chat_by_user(payload.user_email, payload.chat_id, user)
    if not result.is_success:
        raise_bad_request(result.message)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/users", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_role(payload: ChangeRolePayload, user: User = Depends(authenticate)):
    result = await chat_service.change_user_role_by_user(payload.user_email,
                                                         payload.chat_id,
                                                         payload.new_role_type,
                                                         user)
    if not result.is_success:
        raise_bad_request(result.message)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/users", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_from_chat(payload: UserChatPayload, user: User = Depends(authenticate)):
    result = await chat_service.delete_user_from_chat(payload.user_email, payload.chat_id, user)
    if not result.is_success:
        raise_bad_request(result.message)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
