from typing import Dict, Self, Sequence, Type

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session, relationship

from work_schedule_backend.data_structures.permission import PermissionType
from work_schedule_backend.data_structures.user import ServiceType
from work_schedule_backend.db.core import Base


class InvalidFilterColumn(Exception):
    """Request Column is not valid."""


class BaseExpansion:
    @classmethod
    def _get_by_id(cls: Type[Self], session: Session, id) -> Self:
        return session.query(cls).filter(cls.id == id).first()

    @classmethod
    def _find(cls: Type[Self], session: Session, **filters: str) -> Sequence[Self]:
        cls.validate_filters(filters)
        filter_conditions = [
            getattr(cls, k).ilike(f"%{v}%") for k, v in filters.items() if v
        ]

        return session.query(User).filter(*filter_conditions).all()

    @classmethod
    def validate_filters(cls: Type[Self], filters: Dict[str, str]):
        valid_columns = {c.key for c in cls.__table__.columns}
        filters_cols = set(filters.keys())

        if len(filters_cols - valid_columns) > 0:
            raise InvalidFilterColumn("Invalid columns in filter")


class User(Base, BaseExpansion):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    service_type = Column(
        Enum(ServiceType, default=ServiceType.NoService, create_constraint=True)
    )
    permissions = relationship("Permission", back_populates="user")


class Permission(Base, BaseExpansion):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    permission_type = Column(
        Enum(PermissionType, default=PermissionType.Read, create_constraint=True)
    )

    user = relationship("User", back_populates="permissions")
    __table_args__ = (
        UniqueConstraint("user_id", "permission_type", name="uq_user_permission"),
    )
