from pydantic import BaseModel, Field, NonNegativeInt, ValidationError, model_validator
from typing import Optional
from datetime import datetime


class AddTaskRequestModel(BaseModel):
    title: str = Field(max_length=100)
    importance: NonNegativeInt
    deadline: datetime
    est_time_days: Optional[NonNegativeInt]
    description: Optional[str] = Field(max_length=2000)

class TargetSpecificTaskModel(BaseModel):
    task_id: Optional[NonNegativeInt] = None
    title: Optional[str] = Field(max_length=100, default=None)

    @model_validator(mode='after')
    def validate_only_one_field(self):
        if self.task_id and self.title:
            raise ValueError("Cannot provide both title and task_id")
        if not self.task_id and not self.title:
            raise ValueError("Have to provide either task_id or title, neither was provided")
        return self