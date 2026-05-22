"""Audit log model"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class AuditLog(Base):
    """Audit log model for tracking user activities"""
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Action details
    action = Column(String, nullable=False, index=True)  # create, update, delete, login, etc.
    resource_type = Column(String, nullable=False, index=True)  # user, prompt, admin, etc.
    resource_id = Column(String, nullable=True, index=True)
    
    # Additional info
    details = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.action}>"
