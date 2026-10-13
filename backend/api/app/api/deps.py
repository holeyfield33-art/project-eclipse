"""Authentication and role checks for API endpoints."""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.core.rbac import Permission, has_permission
from app.core.security import decode_access_token
from app.services import store

bearer = HTTPBearer(auto_error=False)


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    try:
        claims = decode_access_token(credentials.credentials)
        with store.lock:
            user = store.users.get(str(claims["sub"]))
            if not user or not user["active"] or user["tenant_id"] != claims["tenant_id"] or user["role"] != claims["role"]:
                raise ValueError("Stale or invalid identity")
            return user.copy()
    except (KeyError, ValueError, TypeError, JWTError) as exc:
        # Do not leak token validation details to the client.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials") from exc


def require(permission: Permission):
    def dependency(user: dict = Depends(current_user)) -> dict:
        if not has_permission(user["role"], permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return dependency


def tenant_record(collection: dict, record_id: str, user: dict) -> dict:
    with store.lock:
        item = collection.get(record_id)
        if item is None or item["tenant_id"] != user["tenant_id"]:
            raise HTTPException(status_code=404, detail="Not found")
        return item
