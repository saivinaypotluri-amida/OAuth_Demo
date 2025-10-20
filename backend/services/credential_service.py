from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Optional
from models import Credential, User
from security import encrypt_credentials, decrypt_credentials
from services.slack_service import SlackService
from services.azure_ai_service import AzureAIService
from services.google_service import GoogleWorkspaceService
import logging

logger = logging.getLogger(__name__)


class CredentialService:
    """Service for managing and testing credentials"""
    
    @staticmethod
    async def create_or_update_credential(
        db: Session,
        user_id: int,
        service_type: str,
        credentials: Dict
    ) -> Credential:
        """Create or update credential for a service"""
        # Check if credential already exists
        existing_cred = db.query(Credential).filter(
            Credential.user_id == user_id,
            Credential.service_type == service_type
        ).first()
        
        encrypted_creds = encrypt_credentials(credentials)
        
        if existing_cred:
            # Update existing credential
            existing_cred.encrypted_credentials = encrypted_creds
            existing_cred.is_active = True
            existing_cred.updated_at = datetime.utcnow()
            existing_cred.test_status = "pending"
            db.commit()
            db.refresh(existing_cred)
            return existing_cred
        else:
            # Create new credential
            new_cred = Credential(
                user_id=user_id,
                service_type=service_type,
                encrypted_credentials=encrypted_creds,
                is_active=True,
                test_status="pending"
            )
            db.add(new_cred)
            db.commit()
            db.refresh(new_cred)
            return new_cred
    
    @staticmethod
    async def get_credential(
        db: Session,
        user_id: int,
        service_type: str
    ) -> Optional[Dict]:
        """Get decrypted credentials for a service"""
        credential = db.query(Credential).filter(
            Credential.user_id == user_id,
            Credential.service_type == service_type,
            Credential.is_active == True
        ).first()
        
        if not credential:
            return None
        
        return decrypt_credentials(credential.encrypted_credentials)
    
    @staticmethod
    async def test_credential(
        db: Session,
        user_id: int,
        service_type: str
    ) -> Dict:
        """Test a credential by attempting to connect to the service"""
        credential = db.query(Credential).filter(
            Credential.user_id == user_id,
            Credential.service_type == service_type,
            Credential.is_active == True
        ).first()
        
        if not credential:
            return {
                "status": "failed",
                "message": "Credential not found"
            }
        
        try:
            creds = decrypt_credentials(credential.encrypted_credentials)
            result = None
            
            if service_type == "slack":
                slack_service = SlackService(
                    bot_token=creds.get("bot_token"),
                    signing_secret=creds.get("signing_secret")
                )
                result = await slack_service.test_connection()
            
            elif service_type == "azure_openai":
                azure_service = AzureAIService(
                    endpoint=creds.get("endpoint"),
                    api_key=creds.get("api_key"),
                    deployment=creds.get("deployment"),
                    api_version=creds.get("api_version", "2023-05-15")
                )
                result = await azure_service.test_connection()
            
            elif service_type == "google_workspace":
                google_service = GoogleWorkspaceService(creds)
                result = await google_service.test_connection()
            
            elif service_type == "google_oauth":
                # Validate Google OAuth credentials format
                client_id = creds.get("client_id", "")
                client_secret = creds.get("client_secret", "")
                redirect_uri = creds.get("redirect_uri", "")
                
                if not client_id or not client_secret:
                    result = {
                        "status": "failed",
                        "message": "Client ID and Client Secret are required"
                    }
                elif not client_id.endswith(".apps.googleusercontent.com"):
                    result = {
                        "status": "failed",
                        "message": "Invalid Client ID format. Should end with .apps.googleusercontent.com"
                    }
                elif not client_secret.startswith("GOCSPX-"):
                    result = {
                        "status": "failed",
                        "message": "Invalid Client Secret format. Should start with GOCSPX-"
                    }
                else:
                    result = {
                        "status": "success",
                        "message": "Google OAuth credentials saved. Click 'Connect Google Workspace' to authorize.",
                        "details": {
                            "client_id": client_id,
                            "redirect_uri": redirect_uri
                        }
                    }
            
            else:
                result = {
                    "status": "failed",
                    "message": f"Unknown service type: {service_type}"
                }
            
            # Update credential test results
            credential.last_tested_at = datetime.utcnow()
            credential.test_status = result["status"]
            credential.test_message = result["message"]
            db.commit()
            
            return result
            
        except Exception as e:
            logger.error(f"Error testing credential: {e}")
            credential.last_tested_at = datetime.utcnow()
            credential.test_status = "error"
            credential.test_message = str(e)
            db.commit()
            
            return {
                "status": "error",
                "message": str(e)
            }
    
    @staticmethod
    async def get_all_credentials(db: Session, user_id: int) -> list:
        """Get all credentials for a user (without decrypting)"""
        return db.query(Credential).filter(
            Credential.user_id == user_id
        ).all()
    
    @staticmethod
    async def delete_credential(db: Session, user_id: int, service_type: str) -> bool:
        """Delete a credential"""
        credential = db.query(Credential).filter(
            Credential.user_id == user_id,
            Credential.service_type == service_type
        ).first()
        
        if credential:
            db.delete(credential)
            db.commit()
            return True
        return False
