"""DRF custom exception handling."""
from __future__ import annotations

import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


class ServiceError(APIException):
    """Generic service-layer error."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A service error occurred."
    default_code = "service_error"


class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Resource conflict."
    default_code = "conflict"


class BusinessRuleError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Business rule violated."
    default_code = "business_rule"


def _format_validation_error(exc: ValidationError) -> dict:
    if hasattr(exc, "detail"):
        return exc.detail
    return {"detail": str(exc)}


def api_exception_handler(exc, context):
    """
    Wrap DRF's default handler to:
      - translate Django ``ValidationError`` into DRF ``ValidationError``
      - log 5xx errors
      - always return consistent ``{"detail": ..., "errors": ...}`` shape
    """
    # Django ValidationError → DRF ValidationError
    if isinstance(exc, DjangoValidationError):
        exc = ValidationError(detail=exc.messages)

    # Http404 → DRF NotFound
    if isinstance(exc, Http404):
        exc = NotFound()

    response = drf_exception_handler(exc, context)

    if response is None:
        # Unhandled exception — log and return 500
        logger.exception("Unhandled exception in %s", context.get("view"))
        return Response(
            {"detail": "Internal server error."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Normalise payload shape
    if isinstance(exc, ValidationError):
        response.data = {
            "detail": "Validation failed.",
            "errors": _format_validation_error(exc),
        }
    elif isinstance(exc, (NotAuthenticated, PermissionDenied,
                          NotFound, MethodNotAllowed)):
        if not isinstance(response.data, dict):
            response.data = {"detail": str(exc)}

    # Log 5xx
    if response.status_code >= 500:
        logger.error("5xx in %s: %s", context.get("view"), exc, exc_info=True)

    return response