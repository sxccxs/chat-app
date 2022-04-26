from constants import MIN_CHATNAME_LENGTH, MAX_CHATNAME_LENGTH
from results import Result
from schemas.model_schemas import ChatCreate, ChatEdit


def validate_create_model(chat: ChatCreate) -> Result:
    results = [
        __validate_name(chat.name)
    ]

    invalid_results = tuple(filter(lambda r: not r.is_success, results))

    return invalid_results[0] if invalid_results else Result()


def validate_edit_model(chat: ChatEdit) -> Result:
    results = [
        __validate_name(chat.name)
    ]

    invalid_results = tuple(filter(lambda r: not r.is_success, results))

    return invalid_results[0] if invalid_results else Result()


def __validate_name(name: str) -> Result:
    if name is None or name == "":
        return Result(False, "Chat name can't be empty.")
    if len(name) < MIN_CHATNAME_LENGTH:
        return Result(False, f"Chat name must be at least {MIN_CHATNAME_LENGTH} characters long.")
    if len(name) > MAX_CHATNAME_LENGTH:
        return Result(False, f"Chat name must be less than {MAX_CHATNAME_LENGTH} characters long.")
    return Result()
