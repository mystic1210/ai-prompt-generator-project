"""Authentication schemas"""
from pydantic import BaseModel
from typing import Optional


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    """Login request schema"""
    email: str
    password: str


class TokenData(BaseModel):
    """Token data schema"""
    sub: str  # user_id
    exp: Optional[int] = None
