"""User accounts: registration, login, and the current user."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import User, get_db
from app.schemas import RegisterRequest, UserOut
from app.security import hash_password

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """Create a new account. Fails if the username is already taken."""
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="username already taken")
    user = User(
        username=payload.username,
        name=payload.name,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
