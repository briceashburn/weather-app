from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime, timezone
from http import HTTPStatus


class ApiResponse(BaseModel):
    """
    Global API response model with standardized structure
    """
    code: int = Field(..., description="HTTP status code", example=200)
    message: str = Field(..., description="Response message", example="Success")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Response timestamp in UTC")
    data: Optional[Any] = Field(default=None, description="Response data payload")

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

    @classmethod
    def success(cls, data: Any = None, message: str = "Success", code: int = HTTPStatus.OK) -> "ApiResponse":
        """Create a successful response"""
        return cls(
            code=code,
            message=message,
            data=data
        )

    @classmethod
    def error(cls, message: str, code: int = HTTPStatus.INTERNAL_SERVER_ERROR, data: Any = None) -> "ApiResponse":
        """Create an error response"""
        return cls(
            code=code,
            message=message,
            data=data
        )

    @classmethod
    def not_found(cls, message: str = "Resource not found", data: Any = None) -> "ApiResponse":
        """Create a not found response"""
        return cls(
            code=HTTPStatus.NOT_FOUND,
            message=message,
            data=data
        )

    @classmethod
    def bad_request(cls, message: str = "Bad request", data: Any = None) -> "ApiResponse":
        """Create a bad request response"""
        return cls(
            code=HTTPStatus.BAD_REQUEST,
            message=message,
            data=data
        )

    @classmethod
    def unauthorized(cls, message: str = "Unauthorized", data: Any = None) -> "ApiResponse":
        """Create an unauthorized response"""
        return cls(
            code=HTTPStatus.UNAUTHORIZED,
            message=message,
            data=data
        )

    @classmethod
    def forbidden(cls, message: str = "Forbidden", data: Any = None) -> "ApiResponse":
        """Create a forbidden response"""
        return cls(
            code=HTTPStatus.FORBIDDEN,
            message=message,
            data=data
        )

    @classmethod
    def created(cls, data: Any = None, message: str = "Resource created successfully") -> "ApiResponse":
        """Create a created response"""
        return cls(
            code=HTTPStatus.CREATED,
            message=message,
            data=data
        )

    @classmethod
    def no_content(cls, message: str = "No content") -> "ApiResponse":
        """Create a no content response"""
        return cls(
            code=HTTPStatus.NO_CONTENT,
            message=message,
            data=None
        )
