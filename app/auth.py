"""Authentication utilities for accessing JWT claims from Cognito."""

import jwt
from typing import Any

from fastapi import Request

from app.logger import get_logger

logger = get_logger()


def get_jwt_claims(request: Request) -> dict[str, Any] | None:
    """Extract JWT claims from the Lambda event context or Authorization header.

    Priority:
    1. Lambda event context (API Gateway validated JWT) - production
    2. Authorization header (decoded without validation) - local development

    When API Gateway authenticates a request with a JWT authorizer,
    it passes the decoded JWT claims to Lambda in the event context.
    Mangum makes this available in request.scope['aws.event'].

    For local development, JWT is decoded from the Authorization header
    without verification (verification is done by API Gateway in production).

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
    # Try Lambda event context first (production)
    event = request.scope.get("aws.event")
    if event:
        try:
            claims = event.get("requestContext", {}).get("authorizer", {}).get("jwt", {}).get("claims", {})
            if claims:
                logger.debug("JWT claims extracted from Lambda event", claims_count=len(claims))
                return claims
        except Exception as e:
            logger.error(f"Error extracting JWT claims from Lambda event: {e}", exc_info=True)

    # Fallback to Authorization header (local development)
    auth_header = request.headers.get("authorization")
    if not auth_header:
        logger.debug("No authorization header found")
        return None

    # Extract token from "Bearer <token>"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.debug("Invalid authorization header format", header=auth_header[:20])
        return None

    token = parts[1]

    try:
        # Decode without verification (for local development)
        # In production, API Gateway already validated the JWT
        claims = jwt.decode(token, options={"verify_signature": False})
        logger.debug("JWT claims decoded from Authorization header", claims_count=len(claims))
        return claims
    except Exception as e:
        logger.error(f"Error decoding JWT from Authorization header: {e}", exc_info=True)
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
