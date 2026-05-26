"""
Custom error handlers for the API.

This module manages all exception handlers for the Ninja API,
including HttpError and ValidationError handling.
"""

import logging
from typing import Any, Dict, List

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from ninja.errors import HttpError, ValidationError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

FIVE_HUNDRED = 500


def _create_error_response(
    request,
    messages: List[str],
    status_code: int,
    log_level: int = logging.WARNING,
    use_logger_exception: bool = False,
    extra_log_data: Dict[str, Any] = None,
) -> JsonResponse:
    """
    Helper function to standardize API error logs and JSON responses.
    """
    error_list = [{"msg": msg} for msg in messages]
    log_message = f"API Error {status_code} on {request.method} {request.path} - Messages: {messages}"

    # Track extra context for log aggregators if provided
    extra = extra_log_data or {}

    # 1. Handle Logging based on severity
    if use_logger_exception:
        # Automatically captures and appends the full stack trace (for 500s)
        logger.exception(log_message, extra=extra)
    else:
        logger.log(log_level, log_message, extra=extra)

    # 2. Return standardized JSON structure
    return JsonResponse({"errors": error_list}, status=status_code)


def register_error_handlers(api) -> None:
    """
    Register all custom exception handlers with the NinjaAPI instance.

    Args:
        api: The NinjaAPI instance to register handlers with.
    """

    @api.exception_handler(HttpError)
    def http_error_handler(request, exc: HttpError):
        message = str(exc) if str(exc) else "An HTTP error occurred."
        status_code = exc.status_code
        log_level = logging.ERROR if status_code >= FIVE_HUNDRED else logging.WARNING

        return _create_error_response(request=request, messages=[message], status_code=status_code, log_level=log_level)

    @api.exception_handler(ValidationError)
    def validation_errors(request, exc: ValidationError):
        messages = []
        for err in exc.errors:
            location = " -> ".join(str(loc) for loc in err.get("loc", []))
            msg = err.get("msg", "Unknown error")
            messages.append(f"[{location}]: {msg}" if location else msg)

        return _create_error_response(
            request=request,
            messages=messages,
            status_code=422,
            log_level=logging.ERROR,
            extra_log_data={"validation_errors": exc.errors},
        )

    @api.exception_handler(ObjectDoesNotExist)
    @api.exception_handler(Http404)
    def not_found_error(request, exc):
        message = str(exc) if exc.args else "The requested resource was not found."

        return _create_error_response(request=request, messages=[message], status_code=404, log_level=logging.WARNING)

    @api.exception_handler(Exception)
    def global_generic_error(request, exc: Exception):
        # Keeps internal server errors secure by masking raw system strings

        safe_message = "An unexpected internal server error occurred. Please try again later."

        return _create_error_response(
            request=request,
            messages=[safe_message],
            status_code=FIVE_HUNDRED,
            use_logger_exception=True,  # Triggers logger.exception() for the full traceback
        )
