from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, SlackMessage, Summary
from schemas import (
    SlackMessageRequest,
    SlackMessageResponse,
    SummaryCreate,
    SummaryResponse
)
from security import get_current_user
from services.agent_service import AgentService

router = APIRouter(prefix="/api/agent", tags=["Agent"])


@router.post("/message", response_model=dict)
async def handle_message(
    message_data: SlackMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Handle a message and generate AI response"""
    agent = AgentService(db, current_user.id)
    
    result = await agent.handle_slack_message(
        message=message_data.message,
        channel_id=message_data.channel_id or "direct",
        slack_user_id=str(current_user.id),
        message_ts=str(int(db.query(SlackMessage).count()) + 1)
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to process message")
        )
    
    return result


@router.post("/summary", response_model=dict)
async def create_summary(
    summary_data: SummaryCreate,
    save_to_drive: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a summary and optionally save to Google Drive"""
    agent = AgentService(db, current_user.id)
    
    result = await agent.generate_summary(
        title=summary_data.title,
        content=summary_data.content,
        save_to_drive=save_to_drive
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to generate summary")
        )
    
    return result


@router.get("/messages", response_model=List[SlackMessageResponse])
async def get_messages(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get message history"""
    messages = db.query(SlackMessage).filter(
        SlackMessage.user_id == current_user.id
    ).order_by(SlackMessage.created_at.desc()).offset(offset).limit(limit).all()
    
    return messages


@router.get("/summaries", response_model=List[SummaryResponse])
async def get_summaries(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's summaries"""
    summaries = db.query(Summary).filter(
        Summary.user_id == current_user.id
    ).order_by(Summary.created_at.desc()).offset(offset).limit(limit).all()
    
    return summaries


@router.get("/summaries/{summary_id}", response_model=SummaryResponse)
async def get_summary(
    summary_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific summary"""
    summary = db.query(Summary).filter(
        Summary.id == summary_id,
        Summary.user_id == current_user.id
    ).first()
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )
    
    return summary
