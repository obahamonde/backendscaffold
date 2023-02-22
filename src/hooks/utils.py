"""Utility functions"""

from datetime import datetime
from uuid import uuid4
from random import randint
from secrets import token_urlsafe
from json import dumps, loads


def get_id() -> str:
    """Get a random id."""
    return str(uuid4())


def get_now() -> str:
    """Get the current datetime."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_secret() -> str:
    """Get a random secret."""
    return token_urlsafe(32)


def get_number() -> int:
    """Get a random number."""
    return randint(0, 1000)


def jsonify(data: object) -> dict:
    """Return a json string."""
    if isinstance(data, dict):
        return data
    return loads(dumps(data))