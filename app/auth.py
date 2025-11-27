"""Authentication utilities for accessing JWT claims from Cognito."""

from typing import Any

from fastapi import Request

from app.logger import get_logger

logger = get_logger()


def get_jwt_claims(request: Request) -> dict[str, Any] | None:
    """Extract JWT claims from the Lambda event context.

    When API Gateway authenticates a request with a JWT authorizer,
    it passes the decoded JWT claims to Lambda in the event context.
    Mangum makes this available in request.scope['aws.event'].

    Args:
        request: The FastAPI request object

    Returns:
        Dictionary of JWT claims if available, None otherwise

    Example claims structure:
        {
            'sub': '12345678-1234-1234-1234-123456789012',
            'email': 'user@example.com',
            'email_verified': 'true',
            'cognito:username': 'user@example.com',
            'iss': 'https://cognito-idp.ap-northeast-1.amazonaws.com/...',
            'aud': 'abcdefghijklmnopqrstuvwxyz',
            'token_use': 'access',
            'exp': 1234567890,
            'iat': 1234567890
        }
    """
    event = request.scope.get("aws.event")
    if not event:
        logger.debug("No Lambda event found in request scope")
        return None

    try:
        claims = event.get("requestContext", {}).get("authorizer", {}).get("jwt", {}).get("claims", {})
        if claims:
            logger.debug("JWT claims extracted", claims_count=len(claims))
            return claims
        else:
            logger.debug("No JWT claims found in request context")
            return None
    except Exception as e:
        logger.error(f"Error extracting JWT claims: {e}", exc_info=True)
        return None


def get_user_id(request: Request) -> str | None:
    """Extract the user ID (sub claim) from JWT claims."""
    claims = get_jwt_claims(request)
    return claims.get("sub") if claims else None


def get_user_email(request: Request) -> str | None:
    """Extract the user email from JWT claims."""
    claims = get_jwt_claims(request)
    return claims.get("email") if claims else None


def get_username(request: Request) -> str | None:
    """Extract the Cognito username from JWT claims."""
    claims = get_jwt_claims(request)
    return claims.get("cognito:username") if claims else None
