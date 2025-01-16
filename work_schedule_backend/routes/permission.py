from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from work_schedule_backend.data_structures.permission import PermissionInput
from work_schedule_backend.db.core import get_db

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def _create(
    permission: PermissionInput = Depends(),
    db: Session = Depends(get_db),
) -> PermissionInput:
    return PermissionInput(**permission.create(db, permission.model_dump()).__dict__)
