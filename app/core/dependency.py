from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.jwt_auth import verify_access_token

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    return verify_access_token(credentials.credentials)


def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_security),
):
    if not credentials:
        return None
    try:
        return verify_access_token(credentials.credentials)
    except Exception:
        return None