import functools
import logging
from typing import TypeVar, Protocol

from models.db import database
from results import Result

T = TypeVar("T", bound=Result)
logger = logging.getLogger()


class ResultFunction(Protocol):
    async def __call__(self, *args, **kwargs) -> T: ...


def run_as_transaction(func: ResultFunction) -> ResultFunction:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        transaction = database.transaction()
        try:
            await transaction.start()
            result = await func(*args, **kwargs)
            if not result.is_success:
                await transaction.rollback()
                return result

        except Exception as ex:
            await transaction.rollback()
            logger.exception("Exception happened while executing a transaction. Transaction rolled back.")
            raise ex
        else:
            await transaction.commit()
            logger.info("Transaction committed successfully.")
            return result

    return wrapper
