from sqlalchemy import Column, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from work_schedule_backend.data_structures.permission import PermissionType
from work_schedule_backend.data_structures.user import ServiceType
from work_schedule_backend.db.core import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    service_type = Column(Enum(ServiceType, default=ServiceType.NoService))
    permissions = relationship("Permission", back_populates="user")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    permission_type = Column(Enum(PermissionType, default=PermissionType.Read))

    user = relationship("User", back_populates="permissions")
    __table_args__ = (
        UniqueConstraint("user_id", "permission_type", name="uq_user_permission"),
    )
