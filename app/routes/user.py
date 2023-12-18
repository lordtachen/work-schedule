from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.user import (
    get_user_by_id,
    get_user_by_search_param,
    create_user,
    update_user,
    delete_user,
)

from pydantic import BaseModel, EmailStr

router = APIRouter()


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserInput(UserResponse):
    id: int
    name: str
    email: EmailStr
    hashed_password: str


@router.post("", status_code=status.HTTP_201_CREATED)
def _create_user(
    user: UserInput = Depends(), db: Session = Depends(get_db)
) -> UserResponse:
    return UserResponse(**create_user(db, user.model_dump()).__dict__)


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
    return update_user(db, user_id, user_update.model_dump())


@router.delete("/{user_id}", response_model=UserResponse)
def _delete_user_handler(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user(db, user_id)

@router.get("/{user_id}", response_model=UserResponse)
def _get_user(
    user_id: int, db: Session = Depends(get_db)
):
    user = get_user_by_id(db,user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse( **user.__dict__)