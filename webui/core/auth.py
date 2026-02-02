"""
Authentication Module for DiagnOStiX

Implements HTTP Basic Authentication using secure timing-attack resistant comparison.
"""
import os
import secrets
import logging
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

logger = logging.getLogger(__name__)

security = HTTPBasic()

# Default credentials - MUST be changed in production
DEFAULT_USER = "admin"
DEFAULT_PASS = "diagnostix"

def get_current_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """
    Validate HTTP Basic Credentials against environment variables.
    """
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")

    # Get credentials from env or defaults
    env_user = os.getenv("DIAGNOSTIX_USER", DEFAULT_USER)
    env_pass = os.getenv("DIAGNOSTIX_PASSWORD", DEFAULT_PASS)

    # Log warning if using defaults
    if env_user == DEFAULT_USER and env_pass == DEFAULT_PASS:
        # Only log once per process start ideally, but here we'll log on auth 
        # to ensure it's visible. Using 'debug' to avoid flooding logs after initial startup warning.
        logger.debug("Authentication using default credentials.")

    correct_username_bytes = env_user.encode("utf8")
    correct_password_bytes = env_pass.encode("utf8")

    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        
    return credentials.username

def log_auth_status():
    """Log the authentication status on startup."""
    user = os.getenv("DIAGNOSTIX_USER")
    if not user:
        logger.warning("DIAGNOSTIX_USER not set. Using default: 'admin'")
        logger.warning("DIAGNOSTIX_PASSWORD not set. Using default: 'diagnostix'")
        logger.warning("SECURITY WARNING: Please set these environment variables in production.")
    else:
        logger.info(f"Authentication configured for user: {user}")
