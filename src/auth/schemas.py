from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    login: str
    email: str
    education: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    login: str
    email: str
    education: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False