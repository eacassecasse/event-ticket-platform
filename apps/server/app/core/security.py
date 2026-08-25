from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings


password_hash = PasswordHash.recommended()


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """ Verify a plaintext password against its hash. """

    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def hash_password(password: str) -> str:
    """Hash a password using the configured password hasher."""

    return password_hash.hash(password)


def create_access_token(
    *,
    user_id: int,
    role: str,
) -> str:
    """Create a signed JWT access token."""

    settings = get_settings()

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now
        + timedelta(
            minutes=settings.access_token_expire_minutes,
        ),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""

    settings = get_settings()

    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )