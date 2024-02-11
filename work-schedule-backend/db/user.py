from typing import List, Optional

from sqlalchemy.orm import Session
from app.models import User


def get_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_by_search_param(db: Session, **filters) -> List[User]:
    filter_conditions = [
        getattr(User, k).ilike(f"%{v}%") for k, v in filters.items() if v
    ]
    return db.query(User).filter(*filter_conditions).all()


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
    db_user = get_by_id(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return True
