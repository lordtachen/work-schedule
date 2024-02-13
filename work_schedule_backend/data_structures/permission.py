import enum

from pydantic import BaseModel


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
