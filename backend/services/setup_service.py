import enums
from models.models import RoleType


async def setup() -> None:
    await __setup_role_types()


async def __setup_role_types() -> None:
    for value in enums.RoleType:
        if await RoleType.objects.get_or_none(name=value.name) is None:
            await RoleType.objects.create(name=value.name)
