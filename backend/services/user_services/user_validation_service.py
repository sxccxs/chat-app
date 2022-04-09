import re
import string
from typing import Callable

from results import Result
from schemas.model_schemas import UserCreate


MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 30
MAX_EMAIL_LENGTH = 50
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 50
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

FilterFunc = Callable[[str], bool]


def validate_create_model(user: UserCreate) -> Result:
    results = [
        __validate_username(user.username),
        __validate_email(user.email),
        __validate_password(user.password),
    ]

    invalid_results = tuple(filter(lambda r: not r.is_success, results))

    return invalid_results[0] if invalid_results else Result()


def __validate_username(username: str) -> Result:
    if username is None or username == "":
        return Result(False, "Username can't be empty.")
    if len(username) < MIN_USERNAME_LENGTH:
        return Result(False, f"Username must be at least {MIN_USERNAME_LENGTH} characters long.")
    if len(username) > MAX_USERNAME_LENGTH:
        return Result(False, f"Username must be less than {MAX_USERNAME_LENGTH} characters long.")
    return Result()


def __validate_email(email: str) -> Result:
    if email is None or email == "":
        return Result(False, "Email can't be empty.")
    if not re.match(EMAIL_REGEX, email):
        return Result(False, "Email is in invalid format.")
    if len(email) > MAX_EMAIL_LENGTH:
        return Result(False, f"Email must be less than {MAX_EMAIL_LENGTH} characters long.")
    return Result()


def __validate_password(password: str) -> Result:
    if password is None or password == "":
        return Result(False, "Password can't be empty.")
    if len(password) < MIN_PASSWORD_LENGTH:
        return Result(False, f"Password must be longer than {MIN_PASSWORD_LENGTH} characters.")
    if len(password) > MAX_PASSWORD_LENGTH:
        return Result(False, f"Password can't be longer than {MAX_PASSWORD_LENGTH} characters.")
    if not all((
        __has_alpha_lower(password),
        __has_alpha_upper(password),
        __has_digit(password),
        __has_symbol(password)
    )):
        return Result(False, f"Password must haveat least one lower letter, one upper, a number and a symbol.")

    return Result()


def __has_alpha_lower(item: str) -> bool:
    return __has_condition(item, lambda x: x.isalpha() and x.islower())


def __has_alpha_upper(item: str) -> bool:
    return __has_condition(item, lambda x: x.isalpha() and x.isupper())


def __has_digit(item: str) -> bool:
    return __has_condition(item, lambda x: x.isdigit())


def __has_symbol(item: str) -> bool:
    return __has_condition(item, lambda x: x in string.punctuation)


def __has_condition(item: str, condition: FilterFunc) -> bool:
    return any(map(condition, item))
