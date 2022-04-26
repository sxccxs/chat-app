import base64
import binascii
import secrets
from string import digits, ascii_lowercase
from typing import Any

from fastapi import HTTPException, status

import config


def raise_bad_request(message: str):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


def get_jwt_config_if_exists(dict_key: str):
    """Returns value by given key from 'config.JWT' dict
    if JWT dict exists and given key is specified in it,
    else returns None.
    """
    if not hasattr(config, "JWT"):
        return None
    return config.JWT.get(dict_key)


def get_config_if_exists(key: str) -> Any:
    return getattr(config, key, None)


def constant_time_compare(val1: str, val2: str) -> bool:
    return secrets.compare_digest(force_bytes(val1), force_bytes(val2))


def force_bytes(s) -> bytes:
    if isinstance(s, bytes):
        return s
    return str(s).encode("utf-8", "strict")


def force_str(s) -> str:
    if issubclass(type(s), str):
        return s
    if isinstance(s, bytes):
        return str(s, "utf-8", "strict")

    return str(s)


def urlsafe_base64_encode(s: bytes) -> str:
    return base64.urlsafe_b64encode(s).rstrip(b'\n=').decode('ascii')


def urlsafe_base64_decode(s: str) -> bytes:
    s = s.encode()
    try:
        return base64.urlsafe_b64decode(s.ljust(len(s) + len(s) % 4, b'='))
    except (LookupError, binascii.Error) as e:
        raise ValueError(e)


def base36_to_int(s: str) -> int:
    if len(s) > 13:
        raise ValueError("Base36 input too large")
    return int(s, 36)


def int_to_base36(i):
    char_set = digits + ascii_lowercase
    if i < 0:
        raise ValueError("Negative base36 conversion input.")
    if i < 36:
        return char_set[i]
    b36 = ''
    while i != 0:
        i, n = divmod(i, 36)
        b36 = char_set[n] + b36
    return b36
