from models.models import User, Message, Chat
from results import VResult
from schemas.model_schemas import MessageCreate
from services.chat_services import chat_service
from services.role_services import role_service


async def get_chat_messages(chat: Chat):
    return await Message.objects.select_related(Message.chat).filter(chat=chat).all()


async def create_message(msg: MessageCreate, user: User) -> VResult[Message]:
    chat_result = await chat_service.get_chat_by_id(msg.chat_id)
    if not chat_result.is_success:
        return VResult.from_result(chat_result)

    chat = chat_result.value
    role_result = await role_service.check_user_in_chat(user, chat)
    if not role_result.is_success:
        return VResult.from_result(role_result)

    message = Message(text=msg.text, chat=chat, author=user)
    await message.save()

    return VResult(value=message)


async def get_messages_for_chat_and_user(chat_id: int, user: User) -> VResult[list[Message]]:
    chat_result = await chat_service.get_chat_by_id(chat_id)
    if not chat_result.is_success:
        return VResult.from_result(chat_result)

    chat = chat_result.value
    role_result = await role_service.check_user_in_chat(user, chat)
    if not role_result.is_success:
        return VResult.from_result(role_result)

    messages = await get_chat_messages(chat)

    return VResult(value=messages)