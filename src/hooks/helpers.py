"""Helper classes"""

from typing import Union, Tuple
from base64 import b64encode, b64decode
from jose import jwt
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


def gen_keypair() -> Tuple[str, str]:
    """Key pair generator"""

    key = rsa.generate_private_key(
        backend=crypto_default_backend(), public_exponent=65537, key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption(),
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH
    )

    return private_key.decode("utf-8"), public_key.decode("utf-8")


def jwt_encode(payload: dict, secret: str) -> str:
    """JWT generator"""

    return jwt.encode(payload, secret, algorithm="HS256")


def jwt_decode(token: str, secret: str) -> dict:
    """JWT decoder"""

    return jwt.decode(token, secret, algorithms=["HS256"])


def b64_encode(data: Union[str, bytes, dict]) -> str:
    """Base64 encoder"""

    if isinstance(data, str):
        data = data.encode("utf-8")

    if isinstance(data, dict):
        data = str(data).encode("utf-8")

    return b64encode(data).decode("utf-8")


def b64_decode(data: str) -> Union[str, bytes]:
    """Base64 decoder"""

    return b64decode(data).decode("utf-8")