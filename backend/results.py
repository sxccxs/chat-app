from __future__ import annotations
from typing import Generic, TypeVar

T = TypeVar("T")


class Result:
    def __init__(self, is_success: bool = True, message: str | None = None) -> None:
        self.is_success = is_success
        self.message = message


class VResult(Result, Generic[T]):
    def __init__(self, is_success: bool = True, message: str | None = None, *, value: T = None) -> None:
        super().__init__(is_success, message)
        self.value = value

    @staticmethod
    def create_for_value_or_error(value: T | None, message: str | None) -> VResult[T]:
        return VResult(value=value) if value else VResult(False, message)

    @staticmethod
    def from_result(result: Result) -> VResult[T]:
        return VResult(result.is_success, result.message)
