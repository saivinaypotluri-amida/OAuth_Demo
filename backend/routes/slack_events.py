from fastapi import APIRouter, Request, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from services.credential_service import CredentialService
from services.agent_service import AgentService
from models import User
import hmac
import hashlib
import time
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/slack", tags=["Slack Events"])


def verify_slack_signature(
    signing_secret: str,
    timestamp: str,
    body: bytes,
    signature: str
) -> bool:
    """Verify that request is from Slack"""
    # Prevent replay attacks - reject if timestamp is older than 5 minutes
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False
    
    # Create signature
    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    my_signature = 'v0=' + hmac.new(
        signing_secret.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    return hmac.compare_digest(my_signature, signature)


@router.post("/events")
async def handle_slack_events(
    request: Request,
    x_slack_request_timestamp: str = Header(None),
    x_slack_signature: str = Header(None)
):
    """Handle incoming Slack events"""
    body = await request.body()
    
    try:
        event_data = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Handle URL verification challenge (Slack's way of verifying the endpoint)
    if event_data.get("type") == "url_verification":
        logger.info("Slack URL verification challenge received")
        return {"challenge": event_data.get("challenge")}
    
    # Handle events
    if event_data.get("type") == "event_callback":
        event = event_data.get("event", {})
        event_type = event.get("type")
        
        # Ignore bot messages to prevent loops
        if event.get("bot_id") or event.get("subtype") == "bot_message":
            logger.debug("Ignoring bot message to prevent loop")
            return {"ok": True}
        
        # Get team/workspace info to find the right user's credentials
        team_id = event_data.get("team_id")
        
        # For now, we'll use the first active user's credentials
        # In production, you'd want to map Slack workspace to specific user
        db = SessionLocal()
        try:
            # Find a user with Slack and Azure OpenAI configured
            user = db.query(User).filter(User.is_active == True).first()
            
            if not user:
                logger.error("No active users found")
                return {"ok": False, "error": "No active users"}
            
            # Handle message events
            if event_type == "message":
                await handle_message_event(db, user.id, event)
            
            # Handle app mentions
            elif event_type == "app_mention":
                await handle_mention_event(db, user.id, event)
            
            return {"ok": True}
            
        finally:
            db.close()
    
    return {"ok": True}


async def handle_message_event(db: Session, user_id: int, event: dict):
    """Handle regular message events"""
    channel = event.get("channel")
    text = event.get("text", "")
    user = event.get("user")
    ts = event.get("ts")
    
    # Skip empty messages
    if not text.strip():
        return
    
    # Skip if message is in a thread (to avoid responding to all thread messages)
    if event.get("thread_ts") and event.get("thread_ts") != ts:
        logger.debug("Skipping threaded message")
        return
    
    logger.info(f"Processing message from user {user} in channel {channel}")
    
    # Get agent service
    agent = AgentService(db, user_id)
    
    try:
        # Generate AI response
        result = await agent.handle_slack_message(
            message=text,
            channel_id=channel,
            slack_user_id=user,
            message_ts=ts
        )
        
        if result.get("success"):
            logger.info(f"Successfully responded to message in channel {channel}")
        else:
            logger.error(f"Failed to respond: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"Error handling message: {e}", exc_info=True)


async def handle_mention_event(db: Session, user_id: int, event: dict):
    """Handle app mention events"""
    channel = event.get("channel")
    text = event.get("text", "")
    user = event.get("user")
    ts = event.get("ts")
    
    # Remove the bot mention from the text
    # Example: "<@U1234> hello" -> "hello"
    import re
    text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
    
    if not text:
        text = "Hello! How can I help you?"
    
    logger.info(f"Processing mention from user {user} in channel {channel}")
    
    # Get agent service
    agent = AgentService(db, user_id)
    
    try:
        # Generate AI response
        result = await agent.handle_slack_message(
            message=text,
            channel_id=channel,
            slack_user_id=user,
            message_ts=ts
        )
        
        if result.get("success"):
            logger.info(f"Successfully responded to mention in channel {channel}")
        else:
            logger.error(f"Failed to respond to mention: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"Error handling mention: {e}", exc_info=True)


@router.post("/interactive")
async def handle_slack_interactive(request: Request):
    """Handle Slack interactive components (buttons, menus, etc.)"""
    body = await request.body()
    
    try:
        # Slack sends interactive payloads as form data
        payload = json.loads(body.decode('utf-8').split('payload=')[1])
        
        # Handle different interaction types
        action_type = payload.get("type")
        
        if action_type == "block_actions":
            # Handle button clicks, menu selections, etc.
            logger.info(f"Interactive action received: {payload}")
            
        return {"ok": True}
        
    except Exception as e:
        logger.error(f"Error handling interactive component: {e}")
        return {"ok": False}


@router.post("/slash-commands")
async def handle_slash_command(
    request: Request,
    x_slack_request_timestamp: str = Header(None),
    x_slack_signature: str = Header(None)
):
    """Handle Slack slash commands"""
    form_data = await request.form()
    
    command = form_data.get("command")
    text = form_data.get("text", "")
    user_id = form_data.get("user_id")
    channel_id = form_data.get("channel_id")
    
    logger.info(f"Slash command received: {command} from user {user_id}")
    
    # Example: /ai-summarize [text]
    if command == "/ai-summarize":
        # Handle summary generation
        return {
            "response_type": "in_channel",
            "text": f"Generating summary for: {text[:50]}..."
        }
    
    return {
        "response_type": "ephemeral",
        "text": f"Command {command} received!"
    }
