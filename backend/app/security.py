"""Password hashing and token helpers."""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import ACCESS_TOKEN_TTL_MINUTES, SECRET_KEY

ALGORITHM = "HS256"


def hash_password(password):
    """Return a bcrypt hash for a plaintext password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, password_hash):
    """Check a plaintext password against a stored bcrypt hash."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(user_id):
    """Issue a signed JWT carrying the user id."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_TTL_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token):
    """Return the user id carried in a token, or None if it is invalid or expired."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
    subject = payload.get("sub")
    return int(subject) if subject is not None else None
