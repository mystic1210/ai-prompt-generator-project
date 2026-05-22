"""Prompt model"""
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Prompt(Base):
    """Prompt model for storing generated prompts"""
    __tablename__ = "prompts"

    id = Column(String, primary_key=True, index=True)
    creator_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Prompt content
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    
    # Prompt metadata
    topic = Column(String, nullable=False, index=True)
    audience = Column(String, nullable=False)  # school, college, professional
    skill_level = Column(String, nullable=False)  # beginner, intermediate, advanced
    format = Column(String, nullable=False)  # text, code, tutorial, video, diagram
    
    # Prompt quality
    quality_score = Column(Integer, default=0)
    is_public = Column(Boolean, default=False, index=True)
    is_featured = Column(Boolean, default=False)
    
    # Prompt usage
    usage_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    
    # Generated content metadata
    generated_content_count = Column(Integer, default=0)
    generation_model = Column(String, nullable=True)  # gpt-4, gpt-3.5, claude, etc.
    generation_params = Column(JSON, nullable=True)  # Store API parameters used
    
    # Tags and categories
    tags = Column(String, nullable=True)  # Comma-separated
    category = Column(String, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_used_at = Column(DateTime, nullable=True)
    
    # Relationships
    creator = relationship("User", back_populates="prompts")

    def __repr__(self):
        return f"<Prompt {self.title}>"
