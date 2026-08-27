from typing import Any
from core.database import Base
from datetime import datetime


class ApiResponse(Base):
    success: bool
    status_code: int
    message: str
    data: Any = None
    errors: Any = None
    meta: dict


    def success_response(
        data=None,
        message="Success",
        status_code=200,
        request_id=None,
    ):
        return ApiResponse(
            success=True,
            status_code=status_code,
            message=message,
            data=data,
            errors=None,
            meta={
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": request_id,
            },
        )


    def error_response(
        message,
        errors=None,
        status_code=400,
        request_id=None,
    ):
        return ApiResponse(
            success=False,
            status_code=status_code,
            message=message,
            data=None,
            errors=errors,
            meta={
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": request_id,
            },
        )