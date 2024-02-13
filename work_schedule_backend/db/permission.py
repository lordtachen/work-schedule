from sqlalchemy.orm import Session

from work_schedule_backend.db.models import Permission


def create(db: Session, user_id: int, permission_type: str) -> Permission:
    db_permission = Permission(user_id=user_id, permission_type=permission_type)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission
