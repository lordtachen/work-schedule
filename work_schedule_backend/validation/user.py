from typing import Optional

from pydantic import BaseModel, EmailStr

from work_schedule_backend.models.user import ServiceType


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    service_type: ServiceType


class UserInput(BaseModel):
    name: str
    email: EmailStr
    password: str
    service_type: Optional[ServiceType] = ServiceType.NoService


class UserUpdateInput(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    service_type: Optional[ServiceType] = None
