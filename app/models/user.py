from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum


class ServiceType(enum.Enum):
    Cook = "Cook"
    Waiter = "Waiter"
    Cleaning = "Cleaning"
    NoService = "NoService"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    service_type = Column(Enum(ServiceType, default=ServiceType.NoService))
    permissions = relationship("Permission", back_populates="user")

