from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, AuditLog
from schemas import CredentialCreate, CredentialResponse, CredentialTestResult
from security import get_current_user
from services.credential_service import CredentialService
from datetime import datetime

router = APIRouter(prefix="/api/credentials", tags=["Credentials"])


@router.post("/", response_model=CredentialResponse)
async def create_credential(
    credential_data: CredentialCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update credentials for a service"""
    # Validate service type
    valid_services = ["slack", "azure_openai", "google_workspace", "google_oauth"]
    if credential_data.service_type not in valid_services:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid service type. Must be one of: {', '.join(valid_services)}"
        )
    
    # Create or update credential
    credential = await CredentialService.create_or_update_credential(
        db=db,
        user_id=current_user.id,
        service_type=credential_data.service_type,
        credentials=credential_data.credentials
    )
    
    # Log action
    audit_log = AuditLog(
        user_id=current_user.id,
        action="credential_update",
        resource_type="credential",
        resource_id=str(credential.id),
        details={"service_type": credential_data.service_type},
        status="success"
    )
    db.add(audit_log)
    db.commit()
    
    return credential


@router.get("/", response_model=List[CredentialResponse])
async def get_credentials(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all credentials for current user"""
    credentials = await CredentialService.get_all_credentials(db, current_user.id)
    return credentials


@router.post("/{service_type}/test", response_model=CredentialTestResult)
async def test_credential(
    service_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Test credentials for a service"""
    result = await CredentialService.test_credential(
        db=db,
        user_id=current_user.id,
        service_type=service_type
    )
    
    # Log test action
    audit_log = AuditLog(
        user_id=current_user.id,
        action="credential_test",
        resource_type="credential",
        details={"service_type": service_type, "result": result["status"]},
        status=result["status"]
    )
    db.add(audit_log)
    db.commit()
    
    return {
        "status": result["status"],
        "message": result["message"],
        "tested_at": datetime.utcnow()
    }


@router.delete("/{service_type}")
async def delete_credential(
    service_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete credentials for a service"""
    success = await CredentialService.delete_credential(
        db=db,
        user_id=current_user.id,
        service_type=service_type
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found"
        )
    
    # Log deletion
    audit_log = AuditLog(
        user_id=current_user.id,
        action="credential_delete",
        resource_type="credential",
        details={"service_type": service_type},
        status="success"
    )
    db.add(audit_log)
    db.commit()
    
    return {"message": "Credential deleted successfully"}
