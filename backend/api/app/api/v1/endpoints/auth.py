"""Development-only self-registration: each account receives its own tenant."""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.security import create_access_token, hash_password, verify_password
from app.services import audit, rate_limit, store
from app.core.config import settings

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    full_name: str = Field(min_length=1, max_length=120)


def token_for(user: dict) -> Token:
    return Token(access_token=create_access_token(user["id"], tenant_id=user["tenant_id"], role=user["role"]))


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, request: Request):
    rate_limit.check(request, "login", settings.RATE_LIMIT_LOGIN_PER_MINUTE)
    with store.lock:
        user = next((u for u in store.users.values() if u["email"] == str(payload.email).lower()), None)
        if user is None or not user["active"] or not verify_password(payload.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return token_for(user)


@router.post("/register", response_model=Token, status_code=201)
async def register(payload: UserCreate, request: Request):
    rate_limit.check(request, "register", settings.RATE_LIMIT_REGISTER_PER_MINUTE)
    with store.lock:
        email = str(payload.email).lower()
        if any(u["email"] == email for u in store.users.values()):
            raise HTTPException(status_code=409, detail="Account already exists")
        user = {"id": store.new_id(), "tenant_id": store.new_id(), "email": email,
                "full_name": payload.full_name, "password_hash": hash_password(payload.password),
                "role": "analyst", "active": True}
        store.users[user["id"]] = user
        audit.record(user["tenant_id"], user["id"], "user.register", user["id"])
        return token_for(user)
