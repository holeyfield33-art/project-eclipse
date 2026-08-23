"""Authentication endpoints – JWT + role-based access."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "analyst"  # analyst | manager | admin | auditor


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest):
    # TODO: verify credentials against DB, issue JWT with role claims
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Auth not yet implemented – scaffold only",
    )


@router.post("/register", response_model=Token)
async def register(payload: UserCreate):
    # TODO: create user with hashed password, least-privilege role
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Registration not yet implemented – scaffold only",
    )
