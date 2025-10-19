from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class SlackService:
    def __init__(self, bot_token: str, app_token: Optional[str] = None, signing_secret: Optional[str] = None):
        """Initialize Slack service with credentials"""
        self.bot_token = bot_token
        self.app_token = app_token
        self.signing_secret = signing_secret
        self.client = WebClient(token=bot_token)
        
        # Initialize Bolt app if signing secret is provided
        if signing_secret:
            self.app = App(token=bot_token, signing_secret=signing_secret)
            self.handler = SlackRequestHandler(self.app)
        else:
            self.app = None
            self.handler = None
    
    async def test_connection(self) -> Dict[str, any]:
        """Test Slack connection"""
        try:
            response = self.client.auth_test()
            return {
                "status": "success",
                "message": f"Connected to workspace: {response['team']}",
                "details": {
                    "team": response.get("team"),
                    "user": response.get("user"),
                    "bot_id": response.get("bot_id")
                }
            }
        except SlackApiError as e:
            logger.error(f"Slack connection test failed: {e}")
            return {
                "status": "failed",
                "message": f"Connection failed: {str(e)}",
                "details": None
            }
        except Exception as e:
            logger.error(f"Slack connection test error: {e}")
            return {
                "status": "error",
                "message": f"Error: {str(e)}",
                "details": None
            }
    
    async def send_message(self, channel: str, text: str, thread_ts: Optional[str] = None) -> Dict:
        """Send a message to Slack channel"""
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=text,
                thread_ts=thread_ts
            )
            return {
                "success": True,
                "message_ts": response["ts"],
                "channel": response["channel"]
            }
        except SlackApiError as e:
            logger.error(f"Failed to send Slack message: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_channel_history(self, channel: str, limit: int = 10) -> list:
        """Get channel message history"""
        try:
            response = self.client.conversations_history(
                channel=channel,
                limit=limit
            )
            return response.get("messages", [])
        except SlackApiError as e:
            logger.error(f"Failed to get channel history: {e}")
            return []
    
    async def get_user_info(self, user_id: str) -> Dict:
        """Get Slack user information"""
        try:
            response = self.client.users_info(user=user_id)
            return response.get("user", {})
        except SlackApiError as e:
            logger.error(f"Failed to get user info: {e}")
            return {}
    
    def register_message_handler(self, handler_func):
        """Register a message event handler"""
        if self.app:
            @self.app.event("message")
            def handle_message(event, say):
                handler_func(event, say)
