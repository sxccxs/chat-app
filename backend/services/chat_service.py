from sqlalchemy.orm import Session

import enums
from models import models
from results import VResult
from services import transaction_worker
from services.role_services import role_service


def get_chat_by_id(db: Session, id: int) -> VResult[models.Chat]:
    chat = db.get(models.Chat, id)

    return VResult.create_for_value_or_error(chat, f"Chat with id {id} does not exist.")


def create_chat_by_user(db: Session, user: models.User) -> VResult[models.Chat]:
    return transaction_worker.run_as_transaction(db, lambda s: __create_chat_by_user(s, user))


def __create_chat_by_user(db: Session, user: models.User) -> VResult[models.Chat]:
    chat = models.Chat(users=[user])
    result = role_service.create_role_for_user_and_chat(db, user, chat, enums.RoleType.ADMIN)
    if not result.is_success:
        return VResult.from_result(result)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return VResult(value=chat)
