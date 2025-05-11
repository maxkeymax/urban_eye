from pydantic import BaseModel, EmailStr, Field


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
        None,
        max_length=100,
        examples=["ООО Сириус"],
        description="Необязательное поле"
    )
