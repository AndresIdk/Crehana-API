import json
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: T
    status_code: int

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return json.dumps(self.to_dict())


class ApiResponseError(BaseModel):
    success: bool = False
    error: str
    status_code: int

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return json.dumps(self.to_dict())
