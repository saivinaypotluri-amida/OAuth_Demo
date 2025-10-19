from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from datetime import datetime, timedelta
from database import get_db
from models import User, AuditLog, UsageStats, SlackMessage, Summary
from schemas import (
    UserResponse,
    UserUpdate,
    AuditLogResponse,
    UsageStatsResponse,
    AdminDashboardStats,
    UsageStatsSummary
)
from security import get_current_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard", response_model=AdminDashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics"""
    # Total users
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    # Total messages and summaries
    total_messages = db.query(SlackMessage).count()
    total_summaries = db.query(Summary).count()
    
    # Total tokens and cost
    usage_totals = db.query(
        func.sum(UsageStats.tokens_used).label('total_tokens'),
        func.sum(UsageStats.cost).label('total_cost')
    ).first()
    
    total_tokens_used = usage_totals.total_tokens or 0
    total_cost = float(usage_totals.total_cost or 0)
    
    # Recent logs (last 20)
    recent_logs = db.query(AuditLog).order_by(
        desc(AuditLog.created_at)
    ).limit(20).all()
    
    # Usage by service
    usage_by_service = {}
    service_stats = db.query(
        UsageStats.service_type,
        func.count(UsageStats.id).label('count'),
        func.sum(UsageStats.tokens_used).label('tokens'),
        func.sum(UsageStats.cost).label('cost')
    ).group_by(UsageStats.service_type).all()
    
    for stat in service_stats:
        usage_by_service[stat.service_type] = {
            "count": stat.count,
            "tokens": stat.tokens or 0,
            "cost": float(stat.cost or 0)
        }
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_messages": total_messages,
        "total_summaries": total_summaries,
        "total_tokens_used": total_tokens_used,
        "total_cost": total_cost,
        "recent_logs": recent_logs,
        "usage_by_service": usage_by_service
    }


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get specific user details"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update user details (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    
    user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    
    # Log action
    audit_log = AuditLog(
        user_id=current_user.id,
        action="user_update",
        resource_type="user",
        resource_id=str(user_id),
        details=user_update.dict(exclude_unset=True),
        status="success"
    )
    db.add(audit_log)
    db.commit()
    
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    # Log action
    audit_log = AuditLog(
        user_id=current_user.id,
        action="user_delete",
        resource_type="user",
        resource_id=str(user_id),
        status="success"
    )
    db.add(audit_log)
    db.commit()
    
    return {"message": "User deleted successfully"}


@router.get("/logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    action: str = None,
    user_id: int = None,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get audit logs (admin only)"""
    query = db.query(AuditLog)
    
    if action:
        query = query.filter(AuditLog.action == action)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    
    logs = query.order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()
    return logs


@router.get("/usage", response_model=List[UsageStatsResponse])
async def get_usage_stats(
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    service_type: str = None,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get usage statistics (admin only)"""
    query = db.query(UsageStats)
    
    if user_id:
        query = query.filter(UsageStats.user_id == user_id)
    if service_type:
        query = query.filter(UsageStats.service_type == service_type)
    
    stats = query.order_by(desc(UsageStats.created_at)).offset(skip).limit(limit).all()
    return stats


@router.get("/usage/summary", response_model=UsageStatsSummary)
async def get_usage_summary(
    user_id: int = None,
    days: int = 30,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get usage summary for the specified period"""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(UsageStats).filter(UsageStats.created_at >= since_date)
    if user_id:
        query = query.filter(UsageStats.user_id == user_id)
    
    stats = query.all()
    
    total_messages = len([s for s in stats if s.action_type == "message"])
    total_summaries = len([s for s in stats if s.action_type == "summary"])
    total_tokens = sum(s.tokens_used for s in stats)
    total_cost = sum(s.cost for s in stats)
    
    execution_times = [s.execution_time_ms for s in stats if s.execution_time_ms is not None]
    avg_response_time = sum(execution_times) / len(execution_times) if execution_times else None
    
    return {
        "total_messages": total_messages,
        "total_summaries": total_summaries,
        "total_tokens": total_tokens,
        "total_cost": total_cost,
        "avg_response_time_ms": avg_response_time
    }
