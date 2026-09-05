from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class BaseAPIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[T] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    model_loaded: bool
    disclaimer: str
