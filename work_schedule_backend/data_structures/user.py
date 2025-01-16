import enum

from pydantic import BaseModel, EmailStr


class ServiceType(enum.Enum):
    Cook = "Cook"
    Waiter = "Waiter"
    Cleaning = "Cleaning"
    NoService = "NoService"


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    service_type: ServiceType


class UserInput(BaseModel):
    name: str
    email: EmailStr
    password: str
    service_type: ServiceType | None = ServiceType.NoService


class UserUpdateInput(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    service_type: ServiceType | None = None
