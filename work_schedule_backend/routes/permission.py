from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from work_schedule_backend.db.session import get_db
from work_schedule_backend.models.permission import PermissionInput

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def _create(
    permission: PermissionInput = Depends(), db: Session = Depends(get_db)
) -> PermissionInput:
    return PermissionInput(**permission.create(db, permission.model_dump()).__dict__)
