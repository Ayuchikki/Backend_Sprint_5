from pydantic import BaseModel, Field
from typing import Literal


class LoginModel(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=5)


class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=5)
    role: Literal["admin", "staff"]


class PackageCreate(BaseModel):
    package_name: str = Field(min_length=2)
    destination: str = Field(min_length=2)
    weight: float = Field(gt=0)


class PackageUpdate(BaseModel):
    package_name: str | None = Field(default=None, min_length=2)
    destination: str | None = Field(default=None, min_length=2)
    weight: float | None = Field(default=None, gt=0)
    status: Literal["Pending", "Dispatched", "Delivered"] | None = None


class DispatchCreate(BaseModel):
    destination: str = Field(min_length=2)
    vehicle: str = Field(min_length=2)
    package_ids: list[int] = Field(min_length=1)