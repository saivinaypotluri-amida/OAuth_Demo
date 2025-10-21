from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import datetime
import logging
from models import User, SlackMessage, Summary, AuditLog, UsageStats
from services.credential_service import CredentialService
from services.slack_service import SlackService
from services.azure_ai_service import AzureAIService
from services.google_service import GoogleWorkspaceService

logger = logging.getLogger(__name__)


class AgentService:
    """Main agent service for handling AI interactions"""
    
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
    
    async def _get_services(self) -> Dict:
        """Get all configured services for the user"""
        services = {}
        
        # Get Slack credentials
        slack_creds = await CredentialService.get_credential(
            self.db, self.user_id, "slack"
        )
        if slack_creds:
            services['slack'] = SlackService(
                bot_token=slack_creds.get("bot_token"),
                app_token=slack_creds.get("app_token"),
                signing_secret=slack_creds.get("signing_secret")
            )
        
        # Get Azure AI credentials
        azure_creds = await CredentialService.get_credential(
            self.db, self.user_id, "azure_openai"
        )
        if azure_creds:
            services['azure_ai'] = AzureAIService(
                endpoint=azure_creds.get("endpoint"),
                api_key=azure_creds.get("api_key"),
                deployment=azure_creds.get("deployment"),
                api_version=azure_creds.get("api_version", "2023-05-15")
            )
        
        # Get Google credentials
        google_creds = await CredentialService.get_credential(
            self.db, self.user_id, "google_workspace"
        )
        if google_creds:
            services['google'] = GoogleWorkspaceService(google_creds)
        
        return services
    
    async def handle_slack_message(
        self,
        message: str,
        channel_id: str,
        slack_user_id: str,
        message_ts: str,
        context: Optional[List[str]] = None
    ) -> Dict:
        """Handle incoming Slack message and generate AI response"""
        services = await self._get_services()
        
        if 'azure_ai' not in services:
            return {
                "success": False,
                "error": "Azure AI not configured"
            }
        
        # Generate AI response
        azure_ai = services['azure_ai']
        
        # Build context if provided
        context_str = None
        if context:
            context_str = "\n".join(context)
        
        ai_response = await azure_ai.answer_question(message, context=context_str)
        
        if not ai_response.get("success"):
            return ai_response
        
        response_text = ai_response.get("response")
        tokens_used = ai_response.get("tokens_used", 0)
        execution_time_ms = ai_response.get("execution_time_ms", 0)
        
        # Send response to Slack if available
        if 'slack' in services:
            slack = services['slack']
            await slack.send_message(
                channel=channel_id,
                text=response_text,
                thread_ts=message_ts
            )
        
        # Log the interaction
        slack_msg = SlackMessage(
            user_id=self.user_id,
            slack_user_id=slack_user_id,
            slack_channel_id=channel_id,
            slack_message_ts=message_ts,
            user_message=message,
            bot_response=response_text,
            tokens_used=tokens_used,
            response_time_ms=execution_time_ms
        )
        self.db.add(slack_msg)
        
        # Log usage stats
        usage_stat = UsageStats(
            user_id=self.user_id,
            service_type="azure_openai",
            action_type="message",
            tokens_used=tokens_used,
            cost=tokens_used * 0.00002,  # Approximate cost
            execution_time_ms=execution_time_ms,
            meta_info={"channel_id": channel_id}
        )
        self.db.add(usage_stat)
        
        # Log audit
        audit_log = AuditLog(
            user_id=self.user_id,
            action="slack_message",
            resource_type="message",
            resource_id=message_ts,
            details={"channel": channel_id, "tokens": tokens_used},
            status="success"
        )
        self.db.add(audit_log)
        
        self.db.commit()
        
        return {
            "success": True,
            "response": response_text,
            "tokens_used": tokens_used,
            "execution_time_ms": execution_time_ms
        }
    
    async def generate_summary(
        self,
        title: str,
        content: str,
        save_to_drive: bool = True
    ) -> Dict:
        """Generate a summary and optionally save to Google Drive"""
        services = await self._get_services()
        
        if 'azure_ai' not in services:
            return {
                "success": False,
                "error": "Azure AI not configured"
            }
        
        azure_ai = services['azure_ai']
        
        # Generate summary
        summary_response = await azure_ai.generate_summary(content)
        
        if not summary_response.get("success"):
            return summary_response
        
        summary_text = summary_response.get("response")
        tokens_used = summary_response.get("tokens_used", 0)
        execution_time_ms = summary_response.get("execution_time_ms", 0)
        
        google_drive_file_id = None
        google_drive_file_url = None
        
        # Save to Google Drive if requested and configured
        if save_to_drive and 'google' in services:
            google = services['google']
            doc_result = await google.create_google_doc(
                title=title,
                content=summary_text
            )
            
            if doc_result.get("success"):
                google_drive_file_id = doc_result.get("file_id")
                google_drive_file_url = doc_result.get("file_url")
        
        # Save summary to database
        summary = Summary(
            user_id=self.user_id,
            title=title,
            content=summary_text,
            google_drive_file_id=google_drive_file_id,
            google_drive_file_url=google_drive_file_url
        )
        self.db.add(summary)
        
        # Log usage stats
        usage_stat = UsageStats(
            user_id=self.user_id,
            service_type="azure_openai",
            action_type="summary",
            tokens_used=tokens_used,
            cost=tokens_used * 0.00002,
            execution_time_ms=execution_time_ms
        )
        self.db.add(usage_stat)
        
        # Log audit
        audit_log = AuditLog(
            user_id=self.user_id,
            action="generate_summary",
            resource_type="summary",
            resource_id=str(summary.id),
            details={"title": title, "saved_to_drive": save_to_drive},
            status="success"
        )
        self.db.add(audit_log)
        
        self.db.commit()
        self.db.refresh(summary)
        
        return {
            "success": True,
            "summary": summary_text,
            "summary_id": summary.id,
            "google_drive_file_id": google_drive_file_id,
            "google_drive_file_url": google_drive_file_url,
            "tokens_used": tokens_used,
            "execution_time_ms": execution_time_ms
        }
