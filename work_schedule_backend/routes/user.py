from collections.abc import Sequence

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.params import Query
from sqlalchemy.orm import Session

from work_schedule_backend.data_structures.user import (
    UserInput,
    UserResponse,
    UserUpdateInput,
)
from work_schedule_backend.db import user as db_user
from work_schedule_backend.db.core import get_db

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def _create_user(
    user: UserInput = Body(),
    db: Session = Depends(get_db),
) -> UserResponse:
    return UserResponse(**db_user.create(db, user.model_dump()).__dict__)


@router.get("")
def _get_by_search_params(
    db: Session = Depends(get_db),
    name: str | None = Query(
        None,
        title="name parameter",
        description="Search by name",
    ),
    email: str | None = Query(
        None,
        title="Email parameter",
        description="Search by email",
    ),
) -> Sequence[UserResponse]:
    return db_user.get_by_search_param(db, name=name, email=email)


@router.put("/{user_id}", response_model=UserResponse)
def _update_handler(
    user_id: int,
    user_update: UserUpdateInput,
    db: Session = Depends(get_db),
) -> UserResponse:
    return db_user.update(db, user_id, user_update.model_dump())


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def _delete_user_handler(user_id: int, db: Session = Depends(get_db)) -> None:
    cur_user = db_user.delete(db, user_id)
    if not cur_user:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/{user_id}", response_model=UserResponse)
def _get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    cur_user: UserResponse = db_user.get_by_id(db, user_id)
    if not cur_user:
        raise HTTPException(status_code=404, detail="User not found")
    return cur_user
