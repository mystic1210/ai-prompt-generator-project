"""Prompt schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PromptBase(BaseModel):
    """Base prompt schema"""
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    topic: str
    audience: str  # school, college, professional
    skill_level: str  # beginner, intermediate, advanced
    format: str
    category: str
    tags: Optional[str] = None
    is_public: bool = False


class PromptCreate(PromptBase):
    """Prompt creation schema"""
    content: str = Field(..., min_length=10)


class PromptUpdate(BaseModel):
    """Prompt update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    is_public: Optional[bool] = None
    tags: Optional[str] = None


class PromptResponse(PromptBase):
    """Prompt response schema"""
    id: str
    creator_id: str
    content: str
    quality_score: int
    usage_count: int
    view_count: int
    like_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PromptListResponse(BaseModel):
    """Prompt list item schema"""
    id: str
    title: str
    description: Optional[str]
    topic: str
    audience: str
    format: str
    quality_score: int
    view_count: int
    like_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
