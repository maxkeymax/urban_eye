from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CameraBase(BaseModel):
    camera_id: str = Field(
        ...,
        max_length=50,
        examples=["CAM_001"],
        description="Номер камеры",
    )
    camera_class_cd: int = Field(
        ...,
        examples=[1],
        description="Идентификатор класса камеры",
    )
    camera_class: str = Field(
        ...,
        max_length=100,
        examples=["Класс A"],
        description="Класс камеры",
    )
    model: Optional[str] = Field(
        None,
        max_length=100,
        examples=["Model X"],
        description="Модель камеры (необязательное поле)",
    )
    camera_name: str = Field(
        ...,
        max_length=255,
        examples=["Главная площадь"],
        description="Название камеры",
    )
    camera_place: Optional[str] = Field(
        None,
        max_length=255,
        examples=["ул. Ленина, д. 1"],
        description="Адрес камеры (необязательное поле)",
    )
    camera_place_cd: Optional[int] = Field(
        None,
        examples=[101],
        description="Идентификатор адреса (необязательное поле)",
    )
    serial_number: Optional[str] = Field(
        None,
        max_length=100,
        examples=["SN123456789"],
        description="Серийный номер камеры (необязательное поле)",
    )
    camera_type_cd: int = Field(
        ...,
        examples=[1],
        description="Идентификатор типа камеры",
    )
    camera_type: str = Field(
        ...,
        max_length=100,
        examples=["IP-камера"],
        description="Тип камеры",
    )
    camera_latitude: Optional[float] = Field(
        None,
        examples=[55.7551],
        description="Широта расположения камеры",
    )
    camera_longitude: Optional[float] = Field(
        None,
        examples=[37.6198],
        description="Долгота расположения камеры",
    )
    archive: bool = Field(
        False,
        examples=[False],
        description="Признак архивной камеры",
    )
    azimuth: Optional[int] = Field(
        None,
        examples=[180],
        description="Азимут камеры",
    )


class CameraCreate(CameraBase):
    pass


class CameraResponse(CameraBase):
    id: UUID
    process_dttm: datetime = Field(examples=['"2023-11-20T12:00:00"'])
    model_config = ConfigDict(from_attributes=True)


class CameraUpdate(BaseModel):
    camera_id: Optional[str] = Field(
        default=None,
        max_length=50,
        examples=["CAM_001"],
        description="Номер камеры",
    )
    camera_class_cd: Optional[int] = Field(
        default=None,
        examples=[1],
        description="Идентификатор класса камеры",
    )
    camera_class: Optional[str] = Field(
        default=None,
        max_length=100,
        examples=["Класс A"],
        description="Класс камеры",
    )
    model: Optional[str] = Field(
        default=None,
        max_length=100,
        examples=["Model X"],
        description="Модель камеры (необязательное поле)",
    )
    camera_name: Optional[str] = Field(
        default=None,
        max_length=255,
        examples=["Главная площадь"],
        description="Название камеры",
    )
    camera_place: Optional[str] = Field(
        default=None,
        max_length=255,
        examples=["ул. Ленина, д. 1"],
        description="Адрес камеры (необязательное поле)",
    )
    camera_place_cd: Optional[int] = Field(
        default=None,
        examples=[101],
        description="Идентификатор адреса (необязательное поле)",
    )
    serial_number: Optional[str] = Field(
        default=None,
        max_length=100,
        examples=["SN123456789"],
        description="Серийный номер камеры (необязательное поле)",
    )
    camera_type_cd: Optional[int] = Field(
        default=None,
        examples=[1],
        description="Идентификатор типа камеры",
    )
    camera_type: Optional[str] = Field(
        default=None,
        max_length=100,
        examples=["IP-камера"],
        description="Тип камеры",
    )
    camera_latitude: Optional[float] = Field(
        default=None,
        examples=[55.7551],
        description="Широта расположения камеры",
    )
    camera_longitude: Optional[float] = Field(
        default=None,
        examples=[37.6198],
        description="Долгота расположения камеры",
    )
    archive: Optional[bool] = Field(
        default=None,
        examples=[False],
        description="Признак архивной камеры",
    )
    azimuth: Optional[int] = Field(
        default=None,
        examples=[180],
        description="Азимут камеры",
    )
    
    model_config = ConfigDict(validate_assignment=True)
