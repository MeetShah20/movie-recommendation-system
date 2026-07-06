"""Password hashing and token helpers."""

import bcrypt


def hash_password(password):
    """Return a bcrypt hash for a plaintext password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, password_hash):
    """Check a plaintext password against a stored bcrypt hash."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())
