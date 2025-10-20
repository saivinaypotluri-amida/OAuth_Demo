from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from database import get_db
from models import User, AuditLog
from security import get_current_user
from services.credential_service import CredentialService
from config import settings
import os

router = APIRouter(prefix="/api/oauth", tags=["OAuth"])

# Google OAuth scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]


@router.get("/google/authorize")
async def google_authorize(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initiate Google OAuth flow"""
    # Get Google OAuth credentials from user's stored credentials
    from services.credential_service import CredentialService
    
    google_oauth_creds = await CredentialService.get_credential(
        db=db,
        user_id=current_user.id,
        service_type="google_oauth"
    )
    
    if not google_oauth_creds:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please configure Google OAuth credentials in Settings first"
        )
    
    client_id = google_oauth_creds.get("client_id")
    client_secret = google_oauth_creds.get("client_secret")
    redirect_uri = google_oauth_creds.get("redirect_uri", "http://localhost:8000/api/oauth/google/callback")
    
    if not client_id or not client_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google OAuth credentials are incomplete"
        )
    
    # Create flow instance with user's credentials
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri]
            }
        },
        scopes=SCOPES
    )
    
    flow.redirect_uri = redirect_uri
    
    # Generate authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    # Store state in session (you might want to use a more secure method)
    # For now, we'll pass it in the URL
    authorization_url += f"&state={current_user.id}"
    
    return {
        "authorization_url": authorization_url,
        "state": state
    }


@router.get("/google/callback")
async def google_callback(
    code: str,
    state: str = None,
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback"""
    try:
        # Extract user_id from state
        user_id = int(state) if state else None
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid state parameter"
            )
        
        # Get Google OAuth credentials from user's stored credentials
        from services.credential_service import CredentialService
        
        google_oauth_creds = await CredentialService.get_credential(
            db=db,
            user_id=user_id,
            service_type="google_oauth"
        )
        
        if not google_oauth_creds:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Google OAuth credentials not found"
            )
        
        client_id = google_oauth_creds.get("client_id")
        client_secret = google_oauth_creds.get("client_secret")
        redirect_uri = google_oauth_creds.get("redirect_uri", "http://localhost:8000/api/oauth/google/callback")
        
        # Create flow instance with user's credentials
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            scopes=SCOPES
        )
        
        flow.redirect_uri = redirect_uri
        
        # Exchange code for token
        flow.fetch_token(code=code)
        
        credentials = flow.credentials
        
        # Store credentials
        creds_dict = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes
        }
        
        await CredentialService.create_or_update_credential(
            db=db,
            user_id=user_id,
            service_type="google_workspace",
            credentials=creds_dict
        )
        
        # Log action
        audit_log = AuditLog(
            user_id=user_id,
            action="google_oauth_connected",
            resource_type="credential",
            details={"service": "google_workspace"},
            status="success"
        )
        db.add(audit_log)
        db.commit()
        
        # Redirect to frontend success page
        return RedirectResponse(
            url=f"{settings.allowed_origins.split(',')[0]}/settings?oauth=success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth error: {str(e)}"
        )
