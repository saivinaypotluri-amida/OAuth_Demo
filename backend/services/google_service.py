from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaInMemoryUpload
from typing import Dict, Optional
import logging
import io

logger = logging.getLogger(__name__)


class GoogleWorkspaceService:
    def __init__(self, credentials_dict: Dict):
        """Initialize Google Workspace service with OAuth credentials"""
        self.credentials = Credentials(
            token=credentials_dict.get("token"),
            refresh_token=credentials_dict.get("refresh_token"),
            token_uri=credentials_dict.get("token_uri"),
            client_id=credentials_dict.get("client_id"),
            client_secret=credentials_dict.get("client_secret"),
            scopes=credentials_dict.get("scopes", [
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive"
            ])
        )
    
    async def test_connection(self) -> Dict[str, any]:
        """Test Google Drive connection"""
        try:
            service = build('drive', 'v3', credentials=self.credentials)
            # Try to get user info
            about = service.about().get(fields="user").execute()
            
            return {
                "status": "success",
                "message": f"Connected to Google Drive for user: {about['user']['emailAddress']}",
                "details": {
                    "email": about['user'].get('emailAddress'),
                    "display_name": about['user'].get('displayName')
                }
            }
        except HttpError as e:
            logger.error(f"Google Drive connection test failed: {e}")
            return {
                "status": "failed",
                "message": f"Connection failed: {str(e)}",
                "details": None
            }
        except Exception as e:
            logger.error(f"Google Drive connection test error: {e}")
            return {
                "status": "error",
                "message": f"Error: {str(e)}",
                "details": None
            }
    
    async def create_google_doc(self, title: str, content: str) -> Dict:
        """Create a Google Doc with the given content"""
        try:
            # Create the document using Google Docs API
            docs_service = build('docs', 'v1', credentials=self.credentials)
            drive_service = build('drive', 'v3', credentials=self.credentials)
            
            # Create a new document
            doc = docs_service.documents().create(body={'title': title}).execute()
            doc_id = doc['documentId']
            
            # Insert content into the document
            requests = [{
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': content
                }
            }]
            
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            # Get the web view link
            file = drive_service.files().get(
                fileId=doc_id,
                fields='webViewLink'
            ).execute()
            
            return {
                "success": True,
                "file_id": doc_id,
                "file_url": file.get('webViewLink'),
                "title": title
            }
            
        except HttpError as e:
            logger.error(f"Failed to create Google Doc: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Error creating Google Doc: {e}")
            return {
                "success": False,
                "error": str(e)
    
    async def upload_file_to_drive(
        self,
        filename: str,
        content: str,
        mime_type: str = 'text/plain',
        folder_id: Optional[str] = None
    ) -> Dict:
        """Upload a file to Google Drive"""
        try:
            service = build('drive', 'v3', credentials=self.credentials)
            
            file_metadata = {'name': filename}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaInMemoryUpload(
                content.encode('utf-8'),
                mimetype=mime_type,
                resumable=True
            )
            
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink'
            ).execute()
            
            return {
                "success": True,
                "file_id": file.get('id'),
                "file_url": file.get('webViewLink')
            }
            
        except HttpError as e:
            logger.error(f"Failed to upload file to Drive: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def list_files(self, page_size: int = 10) -> Dict:
        """List files in Google Drive"""
        try:
            service = build('drive', 'v3', credentials=self.credentials)
            
            results = service.files().list(
                pageSize=page_size,
                fields="files(id, name, mimeType, createdTime, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            return {
                "success": True,
                "files": files
            }
            
        except HttpError as e:
            logger.error(f"Failed to list files: {e}")
            return {
                "success": False,
                "error": str(e)
            }
