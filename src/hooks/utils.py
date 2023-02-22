"""Utility functions"""

from datetime import datetime
from uuid import uuid4
from random import randint, choice
from secrets import token_urlsafe
from json import dumps, loads

ascii_chars = """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!()-._?[]{}~;:!@#$%^&*+="""

def get_id() -> str:
    """Get a random id."""
    return str(uuid4())


def get_now() -> datetime:
    """Get the current datetime."""
    return datetime.now()


def get_now_str() -> str:
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

def gen_password(length: int = 16) -> str:
    """Generate a random password."""
    return "".join(choice(ascii_chars) for _ in range(length))