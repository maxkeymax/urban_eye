from typing import List, Optional

from pydantic import BaseModel


class DateRange(BaseModel):
    min: Optional[str]
    max: Optional[str]


class DurationRange(BaseModel):
    min: Optional[float]
    max: Optional[float]


class VideoFiltersResponse(BaseModel):
    upload_date: DateRange
    duration: DurationRange
    time_of_day: List[str]
    status: List[str]
