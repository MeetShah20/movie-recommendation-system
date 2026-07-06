"""People to befriend and the friends list."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import Profile, User, get_db
from app.dependencies import get_current_user
from app.schemas import Person

router = APIRouter()


@router.get("/people", response_model=list[Person])
def list_people(
    search: str = "",
    limit: int = 50,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List profiles and other users that can be added as friends."""
    users = db.query(User).filter(User.id != user.id)
    profiles = db.query(Profile)
    if search:
        users = users.filter(User.name.ilike(f"%{search}%"))
        profiles = profiles.filter(Profile.name.ilike(f"%{search}%"))
    people = [Person(kind="user", id=u.id, name=u.name) for u in users.order_by(User.name).limit(limit)]
    people += [Person(kind="profile", id=p.id, name=p.name) for p in profiles.order_by(Profile.name).limit(limit)]
    return people
