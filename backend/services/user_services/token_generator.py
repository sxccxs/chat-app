from datetime import datetime, timedelta
from hashlib import sha3_256

from models.models import User
from services import util_service

TOKEN_LIFETYME: timedelta = util_service.get_config_if_exists("TOKEN_LIFETYME") or timedelta(hours=5)


class TokenGenerator:
    def make_token(self, user: User) -> str:
        return self._make_token_with_timestamp(
            user,
            self._num_seconds(datetime.now()),
        )

    def check_token(self, user: User, token: str) -> bool:
        if not (user and token):
            return False
        try:
            ts_b36, _ = token.split("-")
            ts = util_service.base36_to_int(ts_b36)
        except ValueError:
            return False

        if not util_service.constant_time_compare(
                self._make_token_with_timestamp(user, ts),
                token,
        ):
            return False
        if (self._num_seconds(datetime.now()) - ts) > TOKEN_LIFETYME.total_seconds():
            return False

        return True

    def _make_token_with_timestamp(self, user: User, timestamp: int) -> str:
        ts_b36 = util_service.int_to_base36(timestamp)
        hash_string = sha3_256(self._make_hash_value(user, timestamp).encode("utf-8")).hexdigest()[::2]
        return f"{ts_b36}-{hash_string}"

    @staticmethod
    def _make_hash_value(user: User, timestamp):
        return f"{user.id}{user.hashed_password}{timestamp}{user.email}"

    @staticmethod
    def _num_seconds(dt: datetime):
        return int((dt - datetime(2001, 1, 1)).total_seconds())
