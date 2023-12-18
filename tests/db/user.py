from sqlalchemy.orm import Session
from app.models.user import User, Permission
from app.db.user import (
    get_user_by_id,
    get_user_by_search_param,
    create_user,
    update_user,
    delete_user,
    create_permission,
)

def test_create_user(db: Session):
    user_data = {"name": "John Doe", "email": "john.doe@example.com", "hashed_password": "hashed_pw"}
    created_user = create_user(db, user_data)
    assert created_user.id is not None

def test_get_user_by_id(db: Session):
    user_data = {"name": "John Doe", "email": "john.doe@example.com", "hashed_password": "hashed_pw"}
    created_user = create_user(db, user_data)

    fetched_user = get_user_by_id(db, created_user.id)
    assert fetched_user is not None
    assert fetched_user.id == created_user.id

def test_get_user_by_search_param(db: Session):
    user_data = {"name": "John Doe", "email": "john.doe@example.com", "hashed_password": "hashed_pw"}
    create_user(db, user_data)

    users = get_user_by_search_param(db, name="John")
    assert len(users) == 1
    assert users[0].name == "John Doe"

def test_update_user(db: Session):
    user_data = {"name": "John Doe", "email": "john.doe@example.com", "hashed_password": "hashed_pw"}
    created_user = create_user(db, user_data)

    update_data = {"name": "Updated Name"}
    updated_user = update_user(db, created_user.id, update_data)
    assert updated_user is not None
    assert updated_user.name == "Updated Name"

def test_delete_user(db: Session):
    user_data = {"name": "John Doe", "email": "john.doe@example.com", "hashed_password": "hashed_pw"}
    created_user = create_user(db, user_data)

    deleted_user = delete_user(db, created_user.id)
    assert deleted_user is not None
    assert deleted_user.id == created_user.id

def test_create_permission(db: Session):
    user_data = {"name": "John Doe", "email": 
