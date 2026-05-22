"""User endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserDetailResponse, UserUpdate
from ..services.user_service import UserService
from ..services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["users"])


def get_current_user(token: str = None, db: Session = Depends(get_db)):
    """Get current user from token"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    token_data = AuthService.decode_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = UserService.get_user_by_id(db, token_data["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/me", response_model=UserDetailResponse)
def get_current_user_profile(current_user = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.patch("/me", response_model=UserDetailResponse)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update current user"""
    updated_user = UserService.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


@router.get("/{user_id}", response_model=UserDetailResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
