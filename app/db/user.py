from typing import List,Optional

from sqlalchemy.orm import Session
from app.models.user import User, Permission


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_search_param(db: Session, **filters) -> List[User]:
    filter_conditions = [
        getattr(User, k).ilike(f"%{v}%") for k, v in filters.items() if v
    ]
    return db.query(User).filter(*filter_conditions).all()


def create_user(db: Session, user_data: dict) -> User:
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_data: dict) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)

    if db_user:
        for key, value in user_data.items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    # ToDO (AM): stil get 500 error when successfully delete
    print("user after delete",db_user)
    return db_user


def create_permission(db: Session, user_id: int, permission_type: str) -> Permission:
    db_permission = Permission(user_id=user_id, permission_type=permission_type)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission
