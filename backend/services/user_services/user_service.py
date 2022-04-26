from hashlib import sha3_256

from models.models import User
from results import VResult, Result
from schemas import model_schemas as schemas
from schemas.model_schemas import PasswordChange, UserCreate, UserUpdate
from services.transaction_worker import run_as_transaction
from services.user_services import user_validation_service, email_service


async def get_user_by_email(email: str) -> VResult[User]:
    user = await User.objects.get_or_none(email=email)
    if not user:
        return VResult(False, f"User with email {email} does not exist")
    return VResult(value=user)


async def update_user(user: User, user_data: schemas.UserUpdate) -> VResult[User]:
    validation_result = user_validation_service.validate_update_model(user_data)
    if not validation_result.is_success:
        return VResult[User].from_result(validation_result)

    if await User.objects.get_or_none(email=user_data.email):
        return VResult[User](False, f"User with email {user.email} already exists.")

    user.username = user_data.username or user.username
    user.email = user_data.email or user.email
    await user.update(["username", "email"])
    await user.load()

    return VResult[User](value=user)


async def change_password(user: User, passwords: PasswordChange) -> VResult[User]:
    validation_result = user_validation_service.validate_password(passwords.new_password)
    if not validation_result.is_success:
        return VResult.from_result(validation_result)

    if not is_password_correct(user, passwords.old_password):
        return VResult(False, "Incorrect password")

    user.hashed_password = __hash_password(passwords.new_password)

    await user.update(["hashed_password"])
    await user.load()

    return VResult(value=user)


@run_as_transaction
async def edit_account_data(user: User, user_data: UserUpdate, activation_url: str | None) -> VResult[User]:
    result = await update_user(user, user_data)
    if not result.is_success or not user_data.email:
        return result

    if not activation_url:
        return VResult(False, "Invalid activation url")

    email_result = await email_service.send_activation_email(activation_url, user)
    if not email_result.is_success:
        return VResult.from_result(email_result)

    return result


@run_as_transaction
async def register(user: UserCreate, activation_url: str) -> Result:
    validation_result = user_validation_service.validate_create_model(user)
    if not validation_result.is_success:
        return VResult.from_result(validation_result)

    if await User.objects.get_or_none(email=user.email):
        return VResult(False, f"User with email {user.email} already exists.")

    user_data = user.dict()
    user_data.pop("password")

    db_user = User(**user_data)
    set_user_password(user.password, db_user)
    await db_user.save()

    email_result = await email_service.send_activation_email(activation_url, db_user)
    if not email_result.is_success:
        return email_result

    return Result()


async def delete_user(user: User) -> None:
    await user.delete()


def is_password_correct(user: User, password: str) -> bool:
    return user.hashed_password == __hash_password(password)


def set_user_password(password: str, user: User) -> None:
    user.hashed_password = __hash_password(password)


def __hash_password(password: str) -> str:
    return sha3_256(password.encode("utf-8")).hexdigest()
