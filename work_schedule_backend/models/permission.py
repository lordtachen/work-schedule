import enum

from pydantic import BaseModel
from sqlalchemy import Column, Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from work_schedule_backend.db.session import Base


class PermissionType(enum.Enum):
    Approve = "Approve"
    Validate = "Validate"
    ManageUsers = "ManageUsers"
    Admin = "Admin"
    Read = "Read"


class PermissionInput(BaseModel):
    id: int
    user_id: int
    permission_type: PermissionType


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    permission_type = Column(Enum(PermissionType, default=PermissionType.Read))

    user = relationship("User", back_populates="permissions")
    __table_args__ = (
        UniqueConstraint("user_id", "permission_type", name="uq_user_permission"),
    )
