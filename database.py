"""Prompt endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.prompt import PromptCreate, PromptUpdate, PromptResponse, PromptListResponse
from ..services.prompt_service import PromptService
from ..services.auth_service import AuthService

router = APIRouter(prefix="/prompts", tags=["prompts"])


def get_current_user_id(token: str = Query(None), db: Session = Depends(get_db)):
    """Get current user ID from token"""
    if not token:
        return None
    
    token_data = AuthService.decode_token(token)
    if not token_data:
        return None
    
    return token_data["user_id"]


@router.post("", response_model=PromptResponse)
def create_prompt(
    prompt_create: PromptCreate,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Create new prompt"""
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    prompt = PromptService.create_prompt(db, current_user_id, prompt_create)
    return prompt


@router.get("/{prompt_id}", response_model=PromptResponse)
def get_prompt(
    prompt_id: str,
    db: Session = Depends(get_db),
):
    """Get prompt by ID"""
    prompt = PromptService.get_prompt_by_id(db, prompt_id)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    # Increment view count
    PromptService.increment_view_count(db, prompt_id)
    db.refresh(prompt)
    
    return prompt


@router.get("/user/me", response_model=list[PromptListResponse])
def get_my_prompts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get current user's prompts"""
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    prompts = PromptService.get_user_prompts(db, current_user_id, skip, limit)
    return prompts


@router.get("", response_model=list[PromptListResponse])
def list_prompts(
    topic: str = Query(None),
    audience: str = Query(None),
    format: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List public prompts with optional filters"""
    if topic or audience or format:
        prompts = PromptService.search_prompts(db, topic, audience, format, skip, limit)
    else:
        prompts = PromptService.get_public_prompts(db, skip, limit)
    
    return prompts


@router.put("/{prompt_id}", response_model=PromptResponse)
def update_prompt(
    prompt_id: str,
    prompt_update: PromptUpdate,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Update prompt"""
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    prompt = PromptService.update_prompt(db, prompt_id, current_user_id, prompt_update)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found or unauthorized"
        )
    
    return prompt


@router.delete("/{prompt_id}")
def delete_prompt(
    prompt_id: str,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Delete prompt"""
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    success = PromptService.delete_prompt(db, prompt_id, current_user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found or unauthorized"
        )
    
    return {"message": "Prompt deleted successfully"}


@router.post("/{prompt_id}/like")
def like_prompt(
    prompt_id: str,
    db: Session = Depends(get_db)
):
    """Like a prompt"""
    prompt = PromptService.get_prompt_by_id(db, prompt_id)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prompt not found"
        )
    
    PromptService.like_prompt(db, prompt_id)
    db.refresh(prompt)
    
    return {"message": "Prompt liked", "likes": prompt.like_count}
