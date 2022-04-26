import enums
from models.models import Role, User, Chat, RoleType
from results import VResult, Result


async def create_role_for_user_and_chat(user: User, chat: Chat,
                                        role_type: enums.RoleType = enums.RoleType.MEMBER) -> VResult[Role]:
    if await get_role_for_user_and_chat(user, chat):
        return VResult(False, f"User {user.id} and chat {chat.id} already have a role.")

    role_type = await RoleType.objects.get(name=role_type.name)
    role = Role(user=user, chat=chat, role_type=role_type)
    await role.save()

    return VResult[Role]()


async def get_role_for_user_and_chat(user: User, chat: Chat) -> Role | None:
    return await Role.objects.select_related(Role.role_type).get_or_none(user=user, chat=chat)


async def check_user_and_chat_role(user: User, chat: Chat,
                                   role_type: enums.RoleType = enums.RoleType.MEMBER) -> Result:
    role_result = await check_user_in_chat(user, chat)
    if not role_result.is_success:
        return role_result

    if role_result.value.role_type.name != role_type.name:
        return Result(False, "User does not have rights for this operation")
    return Result()


async def check_user_in_chat(user: User, chat: Chat) -> VResult[Role]:
    role = await get_role_for_user_and_chat(user, chat)
    return VResult(value=role) if role else VResult(False, "User is not in chat")


async def check_if_last_admin_in_chat(user: User, chat: Chat) -> bool:
    admins = await Role.objects.select_related([Role.user, Role.chat, Role.role_type]) \
        .filter(chat=chat, role_type__name=enums.RoleType.ADMIN.name) \
        .exclude(user=user).all()
    return len(admins) == 0


async def check_if_last_user_in_chat(user: User, chat: Chat) -> bool:
    users = await Role.objects.select_related([Role.user, Role.chat]) \
        .filter(chat=chat) \
        .exclude(user=user).all()
    return len(users) == 0
