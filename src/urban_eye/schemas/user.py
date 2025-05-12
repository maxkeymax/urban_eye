import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        max_length=255,
        examples=["user@example.com"],
        description="Должен быть уникальным",
    )
    user_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Иван Иванов"],
        description="Полное имя пользователя",
    )
    organization: str | None = Field(
        None, max_length=100, examples=["ООО Сириус"], description="Необязательное поле"
    )


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["Str0ngP@ss"],
        description="Должен содержать заглавные буквы и цифры",
        pattern=r"^(?=.*[A-Z])(?=.*\d).+$",
    )


class UserResponse(UserBase):
    id: int = Field(examples=[1])
    is_active: bool = Field(examples=[True])
    created_at: datetime = Field(examples=["2023-11-20T12:00:00"])
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(
        default=None,
        max_length=255,
        examples=["user@example.com"],
        description="Должен быть уникальным",
    )
    user_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        examples=["Иван Иванов"],
        description="Полное имя пользователя",
    )
    organization: Optional[str] = Field(
        default=None,
        max_length=100,
        examples=["ООО Сириус"],
        description="Необязательное поле",
    )
    is_active: Optional[bool] = Field(default=None)

    model_config = ConfigDict(validate_assignment=True)
    