from typing import Callable, TypeVar

from sqlalchemy.orm import Session

from results import Result

T = TypeVar("T", bound=Result)
ResultFunction = Callable[[Session], T]


def run_as_transaction(db: Session, f: ResultFunction) -> T:
    try:
        db.begin()
        result = f(db)
        if not result.is_success:
            db.rollback()
        else:
            db.commit()

        return result
    except Exception as ex:
        db.rollback()

        return type(T)(False, str(ex))
    finally:
        db.close()
