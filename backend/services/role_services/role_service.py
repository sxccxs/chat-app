from sqlalchemy.orm import Session

import enums
from models.models import Role, User, Chat
from results import VResult
from services.role_services import role_type_service


def get_role_by_id(db: Session, id: int) -> VResult[Role]:
    role = db.get(Role, id)
    return VResult(value=role) if role else VResult(False, f"Role with id {id} does not exist.")


def create_role_for_user_and_chat(db: Session, user: User, chat: Chat,
                                  role_type: enums.RoleType = enums.RoleType.MEMBER) -> VResult[Role]:
    if chat in user.chats:
        return VResult(False, f"User {user.id} and chat {chat.id} already have a role.")

    role_type = role_type_service.get_role_type_by_name(db, role_type.name)
    role = Role(user=user, chat=chat, role_type=role_type)
    db.add(role)
    db.commit()
    db.refresh(role)

    return VResult[Role]()
