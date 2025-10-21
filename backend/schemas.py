from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Credential Schemas
class CredentialBase(BaseModel):
    service_type: str
    credentials: Dict[str, Any]


class CredentialCreate(CredentialBase):
    pass


class CredentialUpdate(BaseModel):
    credentials: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class CredentialResponse(BaseModel):
    id: int
    service_type: str
    is_active: bool
    last_tested_at: Optional[datetime] = None
    test_status: Optional[str] = None
    test_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class CredentialTestResult(BaseModel):
    status: str
    message: str
    tested_at: datetime


# Slack Schemas
class SlackMessageRequest(BaseModel):
    message: str
    channel_id: Optional[str] = None


class SlackMessageResponse(BaseModel):
    id: int
    user_message: str
    bot_response: str
    tokens_used: int
    response_time_ms: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Summary Schemas
class SummaryCreate(BaseModel):
    title: str
    content: str
    source_messages: Optional[List[str]] = None


class SummaryResponse(BaseModel):
    id: int
    title: str
    content: str
    google_drive_file_id: Optional[str] = None
    google_drive_file_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Audit Log Schemas
class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Usage Stats Schemas
class UsageStatsResponse(BaseModel):
    id: int
    user_id: int
    service_type: str
    action_type: str
    tokens_used: int
    cost: float
    execution_time_ms: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UsageStatsSummary(BaseModel):
    total_messages: int
    total_summaries: int
    total_tokens: int
    total_cost: float
    avg_response_time_ms: Optional[float] = None


# Admin Schemas
class AdminDashboardStats(BaseModel):
    total_users: int
    active_users: int
    total_messages: int
    total_summaries: int
    total_tokens_used: int
    total_cost: float
    recent_logs: List[AuditLogResponse]
    usage_by_service: Dict[str, Any]


# OAuth Schemas
class GoogleOAuthCallback(BaseModel):
    code: str
    state: Optional[str] = None


class GoogleOAuthResponse(BaseModel):
    status: str
    message: str
    file_url: Optional[str] = None
