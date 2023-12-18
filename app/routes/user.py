from typing import List, Optional
from fastapi import APIRouter, Depends, status
from fastapi.params import Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.user import (
    get_user_by_search_param,
    create_user,
    update_user,
    delete_user,
)

from pydantic import BaseModel

router = APIRouter()


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class UserInput(UserResponse):
    hashed_password: str


@router.post("", status_code=status.HTTP_201_CREATED)
def _create_user(user: UserInput, db: Session = Depends(get_db)) -> UserResponse:
    user_data = user.model_dump()
    out_user = create_user(db, user_data).__dict__
    return UserResponse(**out_user)


@router.get("")
def _get_user_by_search_params(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(
        None, title="name parameter", description="Search by name"
    ),
    email: Optional[str] = Query(
        None, title="Email parameter", description="Search by email"
    ),
) -> List[UserResponse]:
    return get_user_by_search_param(db, name=name, email=email)


@router.put("/{user_id}", response_model=UserResponse)
def _update_user_handler(
    user_id: int, user_update: UserInput, db: Session = Depends(get_db)
):
    user_data = user_update.model_dump(exclude_unset=True)
    return update_user(db, user_id, user_data)


@router.delete("/{user_id}", response_model=UserResponse)
def _delete_user_handler(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
