from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.database import User, AuthLog, Prompt, PostLog, UserRole
from app.schemas.auth import UserResponse
from app.routers.auth import get_current_user
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["admin"])

async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin resources"
        )
    return current_user

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user)
):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users

@router.get("/auth-logs")
async def get_auth_logs(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
    days: int = 7
):
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    logs = db.query(AuthLog).filter(
        AuthLog.timestamp >= cutoff_date
    ).order_by(AuthLog.timestamp.desc()).all()
    
    return [{
        "id": log.id,
        "user_id": log.user_id,
        "user_email": log.user.email if log.user else None,
        "method": log.method,
        "status": log.status,
        "error_message": log.error_message,
        "timestamp": log.timestamp
    } for log in logs]

@router.get("/content-stats")
async def get_content_stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
    days: int = 7
):
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Get prompts
    prompts = db.query(Prompt).filter(
        Prompt.created_at >= cutoff_date
    ).order_by(Prompt.created_at.desc()).all()
    
    # Get posts
    posts = db.query(PostLog).filter(
        PostLog.timestamp >= cutoff_date
    ).order_by(PostLog.timestamp.desc()).all()
    
    return {
        "total_prompts": len(prompts),
        "total_posts": len(posts),
        "prompts": [{
            "id": p.id,
            "user_email": p.user.email,
            "input_text": p.input_text,
            "created_at": p.created_at
        } for p in prompts],
        "posts": [{
            "id": p.id,
            "user_email": p.user.email,
            "platform": p.platform,
            "status": p.status,
            "error": p.error,
            "timestamp": p.timestamp
        } for p in posts]
    }

@router.get("/user/{user_id}/activity")
async def get_user_activity(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's auth logs
    auth_logs = db.query(AuthLog).filter(
        AuthLog.user_id == user_id
    ).order_by(AuthLog.timestamp.desc()).all()
    
    # Get user's prompts
    prompts = db.query(Prompt).filter(
        Prompt.user_id == user_id
    ).order_by(Prompt.created_at.desc()).all()
    
    # Get user's posts
    posts = db.query(PostLog).filter(
        PostLog.user_id == user_id
    ).order_by(PostLog.timestamp.desc()).all()
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "is_verified": user.is_verified,
            "created_at": user.created_at,
            "connected_accounts": user.connected_accounts_json
        },
        "auth_logs": [{
            "method": log.method,
            "status": log.status,
            "error_message": log.error_message,
            "timestamp": log.timestamp
        } for log in auth_logs],
        "prompts": [{
            "id": p.id,
            "input_text": p.input_text,
            "created_at": p.created_at
        } for p in prompts],
        "posts": [{
            "id": p.id,
            "platform": p.platform,
            "status": p.status,
            "error": p.error,
            "timestamp": p.timestamp
        } for p in posts]
    } 