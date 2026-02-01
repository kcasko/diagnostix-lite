"""Optional API key authentication."""
import os
from fastapi import HTTPException, Request, status

API_KEY_HEADER = "X-API-Key"


def require_api_key(request: Request) -> None:
    expected = os.getenv("DIAGNOSTIX_API_KEY")
    if not expected:
        return
    provided = request.headers.get(API_KEY_HEADER)
    if provided != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
