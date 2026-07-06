"""People to befriend and the friends list."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import Friendship, Profile, User, get_db
from app.dependencies import get_current_user
from app.schemas import AddFriendRequest, Person

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


def _link(db, owner_id, kind, friend_id):
    """Create a friendship if it does not already exist."""
    exists = (
        db.query(Friendship)
        .filter_by(owner_id=owner_id, friend_kind=kind, friend_id=friend_id)
        .first()
    )
    if exists is None:
        db.add(Friendship(owner_id=owner_id, friend_kind=kind, friend_id=friend_id))


def _friends_of(db, owner_id):
    """Resolve a user's friendships into people with names."""
    people = []
    for row in db.query(Friendship).filter_by(owner_id=owner_id).all():
        if row.friend_kind == "profile":
            profile = db.get(Profile, row.friend_id)
            if profile is not None:
                people.append(Person(kind="profile", id=profile.id, name=profile.name))
        else:
            other = db.get(User, row.friend_id)
            if other is not None:
                people.append(Person(kind="user", id=other.id, name=other.name))
    return people


@router.get("/friends", response_model=list[Person])
def my_friends(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Return the current user's friends."""
    return _friends_of(db, user.id)


@router.post("/friends", response_model=list[Person])
def add_friend(
    payload: AddFriendRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Add a profile or another user as a friend, then return the updated list."""
    if payload.kind == "profile":
        if db.get(Profile, payload.id) is None:
            raise HTTPException(status_code=404, detail="profile not found")
    elif payload.kind == "user":
        if payload.id == user.id or db.get(User, payload.id) is None:
            raise HTTPException(status_code=400, detail="invalid user")
    else:
        raise HTTPException(status_code=400, detail="invalid kind")

    _link(db, user.id, payload.kind, payload.id)
    if payload.kind == "user":
        _link(db, payload.id, "user", user.id)
    db.commit()
    return _friends_of(db, user.id)
