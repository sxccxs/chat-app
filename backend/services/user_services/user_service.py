from hashlib import sha3_256

from sqlalchemy.orm import Session

from models.db import session_maker
from models.models import User
from results import Result, VResult
from schemas import model_schemas as schemas
from services.user_services import user_validation_service


def get_user_by_id(db: Session, id: int) -> VResult[User]:
    user = db.get(User, id)

    return VResult.create_for_value_or_error(user, f"User with id {id} does not exist.")


def get_user_by_email(db: Session, email: str) -> VResult[User]:
    user = db.query(User).filter_by(email=email).first()

    return VResult.create_for_value_or_error(user, f"User with email {email} does not exist.")


def get_active_user_by_id(db: Session, id: int) -> VResult[User]:
    user = db.query(User).filter_by(is_active=True, id=id).first()

    return VResult.create_for_value_or_error(user, f"User with id {id} does not exist.")


def get_active_user_by_email(db: Session, email: str) -> VResult[User]:
    user = db.query(User).filter_by(is_active=True, email=email).first()

    return VResult.create_for_value_or_error(user, f"User with email {email} does not exist.")


def create_user(db: Session, user: schemas.UserCreate) -> VResult[User]:
    validation_result = user_validation_service.validate_create_model(user)
    if not validation_result.is_success:
        return VResult.from_result(validation_result)

    if get_user_by_email(db, user.email).is_success:
        return VResult(False, f"User with email {user.email} already exists.")

    hashed_password = __hash_password(user.password)
    user_data = user.dict()
    user_data.pop("password")

    db_user = User(**user_data, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return VResult(value=db_user)


def update_user(db: Session, user_data: schemas.UserUpdate) -> Result:
    user: User | None = db.get(User, user_data.id)
    if user:
        user.username = user_data.username or user.username
        user.email = user_data.email or user.email
        user.is_active = user_data.is_active or user.is_active
        user.hashed_password = __hash_password(user_data.password) or user.hashed_password

        return Result()

    return Result(False, f"User with id {user_data.id} does not exist")


def delete_user(db: Session, id: int) -> None:
    db.get(User, id).delete()
    db.commit()


def check_password(user: User, password: str) -> bool:
    return user.hashed_password == __hash_password(password)


def __hash_password(password: str) -> str:
    return sha3_256(password.encode("utf-8")).hexdigest()
