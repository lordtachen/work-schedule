from typing import Any, Optional, Sequence

from sqlalchemy.orm import Session

from work_schedule_backend.data_structures.user import UserResponse
from work_schedule_backend.db.models import User


def get_by_id(db: Session, user_id: int) -> UserResponse | None:
    user: Optional[UserResponse] = User._get_by_id(db, user_id)
    if user:
        return UserResponse(**user.__dict__)
    return None


def get_by_search_param(
    db: Session,
    **filters: dict[str, Any],
) -> Sequence[UserResponse]:
    return [UserResponse(**user.__dict__) for user in User._find(db, **filters)]


def create(db: Session, user_data: dict) -> User:
    password = user_data.pop("password")
    db_user = User(**(user_data | {"hashed_password": password}))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update(db: Session, user_id: int, user_data: dict) -> Optional[User]:
    db_user = get_by_id(db, user_id)

    if db_user:
        for key, value in user_data.items():
            if value is not None:
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)

    return db_user


def delete(db: Session, user_id: int) -> Optional[bool]:
    user = User._get_by_id(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return True
