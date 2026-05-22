"""User schemas"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    bio: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UserResponse(UserBase):
    """User response schema"""
    id: str
    is_active: bool
    is_verified: bool
    subscription_tier: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Detailed user response"""
    bio: Optional[str]
    profile_picture_url: Optional[str]
    company: Optional[str]
    website: Optional[str]
    last_login: Optional[datetime]
    updated_at: datetime
