from sqlalchemy.orm import Session

import enums
from models.db import session_maker
from services.role_services import role_type_service


def setup() -> None:
    with session_maker() as session:
        __setup_role_types(session)


def __setup_role_types(db: Session) -> None:
    for value in enums.RoleType:
        if role_type_service.get_role_type_by_name(db, value.name) is None:
            role_type_service.create_role_type(db, value.name)
