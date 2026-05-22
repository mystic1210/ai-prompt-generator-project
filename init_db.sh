"""User service"""
import uuid
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service for user operations"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create new user"""
        db_user = User(
            id=str(uuid.uuid4()),
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            hashed_password=UserService.hash_password(user_create.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update_user(db: Session, user_id: str, user_update: UserUpdate) -> User:
        """Update user"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db_user.updated_at = datetime.utcnow()
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_last_login(db: Session, user_id: str) -> None:
        """Update last login timestamp"""
        db_user = UserService.get_user_by_id(db, user_id)
        if db_user:
            db_user.last_login = datetime.utcnow()
            db.add(db_user)
            db.commit()
