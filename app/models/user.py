from sqlalchemy import Column, Integer, String, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class ServiceType(enum.Enum):
    Cook = "Cook"
    Waiter = "Waiter"
    Cleaning = "Cleaning"
    NoService = "NoService"


class PermissionType(enum.Enum):
    Approve = "Approve"
    Validate = "Validate"
    ManageUsers = "ManageUsers"
    Admin = "Admin"
    Read = "Read"


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    permission_type = Column(Enum(PermissionType, default=PermissionType.Read))

    user = relationship("User", back_populates="permissions")
    __table_args__ = (
        UniqueConstraint("user_id", "permission_type", name="uq_user_permission"),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    service_type = Column(Enum(ServiceType, default=ServiceType.NoService))
    permissions = relationship("Permission", back_populates="user")
