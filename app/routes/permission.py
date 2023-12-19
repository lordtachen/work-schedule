from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.permission import PermissionInput


router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED)
def _create(
    permission: PermissionInput = Depends(), db: Session = Depends(get_db)
) -> PermissionInput:
    return PermissionInput(**permission.create(db, permission.model_dump()).__dict__)