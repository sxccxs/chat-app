import enums
from models.models import Chat, User, RoleType, Role
from results import VResult, Result
from schemas.model_schemas import ChatCreate, ChatEdit
from services.chat_services import chat_validation_service
from services.role_services import role_service
from services.transaction_worker import run_as_transaction
from services.user_services import user_service


async def get_user_chats(user: User) -> list[Chat]:
    return (await User.objects.select_related("chats").get(id=user.id)).chats


async def get_chat_by_id(chat_id: int) -> VResult[Chat]:
    chat = await Chat.objects.get_or_none(id=chat_id)
    if not chat:
        return VResult(False, f"Chat with id {chat_id} does not exist.")
    return VResult(value=chat)


async def get_chat_users(chat_id: int, user: User) -> VResult[list[User]]:
    chat = await Chat.objects.select_related(Chat.users).get_or_none(id=chat_id)
    if not chat:
        return VResult(False, f"Chat with id {chat_id} does not exist.")

    role = await role_service.get_role_for_user_and_chat(user, chat)
    if not role:
        return VResult(False, f"User does not belong to chat")

    return VResult(value=chat.users)


@run_as_transaction
async def create_chat_by_user(chat_data: ChatCreate, user: User) -> VResult[Chat]:
    validation_result = chat_validation_service.validate_create_model(chat_data)
    if not validation_result.is_success:
        return VResult.from_result(validation_result)

    chat = await Chat.objects.create(**chat_data.dict())
    await chat.users.add(user)

    result = await role_service.create_role_for_user_and_chat(user, chat, enums.RoleType.ADMIN)
    if not result.is_success:
        return VResult.from_result(result)

    return VResult(value=chat)


async def edit_chat_by_user(chat_data: ChatEdit, user: User) -> VResult[Chat]:
    validation_result = chat_validation_service.validate_edit_model(chat_data)
    if not validation_result.is_success:
        return VResult.from_result(validation_result)

    chat_result = await get_chat_by_id(chat_data.id)
    if not chat_result.is_success:
        return chat_result

    chat = chat_result.value
    result = await role_service.check_user_and_chat_role(user, chat, enums.RoleType.ADMIN)
    if not result.is_success:
        return VResult.from_result(result)

    chat.name = chat_data.name
    await chat.update()

    return VResult(value=chat)


@run_as_transaction
async def delete_chat_by_user(chat_id: int, user: User) -> Result:
    chat_result = await __get_chat_and_check_user_rights(chat_id, user)
    if not chat_result.is_success:
        return chat_result

    chat = chat_result.value

    if (await role_service.check_if_last_admin_in_chat(user, chat) and
            not await role_service.check_if_last_user_in_chat(user, chat)):
        return Result(False, "Can't delete last admin from chat")

    role = await role_service.get_role_for_user_and_chat(user, chat)
    await role.delete()
    await chat.delete()

    return Result()


@run_as_transaction
async def add_user_to_chat_by_user(user_email: str, chat_id: int, by_user: User) -> Result:
    chat_result = await __get_chat_and_check_user_rights(chat_id, by_user)
    if not chat_result.is_success:
        return chat_result

    chat = chat_result.value

    user_result = await user_service.get_user_by_email(user_email)
    if not user_result.is_success:
        return user_result

    user = user_result.value
    role_result = await role_service.create_role_for_user_and_chat(user, chat, enums.RoleType.MEMBER)
    if not role_result.is_success:
        return role_result

    await chat.users.add(user)

    return Result()


async def change_user_role_by_user(user_email: str, chat_id, new_role: enums.RoleType, by_user: User) -> Result:
    result = await __get_role_chat_user(user_email, chat_id, by_user)
    if not result.is_success:
        return result

    role, *_ = result.value
    role.role_type = await RoleType.objects.get(name=new_role.name)
    await role.update()

    return Result()


@run_as_transaction
async def delete_user_from_chat(user_email: str, chat_id: int, by_user: User) -> Result:
    result = await __get_role_chat_user(user_email, chat_id, by_user)
    if not result.is_success:
        return result

    user, chat, role = result.value
    await role.delete()
    await chat.users.remove(user)

    return Result()


async def __get_chat_and_check_user_rights(chat_id: int, user: User) -> VResult[Chat]:
    chat_result = await get_chat_by_id(chat_id)
    if not chat_result.is_success:
        return chat_result

    chat = chat_result.value
    result = await role_service.check_user_and_chat_role(user, chat, enums.RoleType.ADMIN)
    if not result.is_success:
        return VResult.from_result(result)

    return VResult(value=chat)


async def __get_role_chat_user(user_email: str, chat_id: int, by_user: User) -> VResult[tuple[User, Chat, Role]]:
    chat_result = await __get_chat_and_check_user_rights(chat_id, by_user)
    if not chat_result.is_success:
        return VResult.from_result(chat_result)

    chat = chat_result.value
    user_result = await user_service.get_user_by_email(user_email)
    if not user_result.is_success:
        return VResult.from_result(user_result)

    user = user_result.value
    role = await role_service.get_role_for_user_and_chat(user, chat)
    if role is None:
        return VResult(False, "User does not belong to chat")

    return VResult(value=(user, chat, role))
