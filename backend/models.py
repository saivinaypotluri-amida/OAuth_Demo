from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="user")  # 'user' or 'admin'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    credentials = relationship("Credential", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    usage_stats = relationship("UsageStats", back_populates="user", cascade="all, delete-orphan")
    summaries = relationship("Summary", back_populates="user", cascade="all, delete-orphan")


class Credential(Base):
    __tablename__ = "credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_type = Column(String, nullable=False)  # 'slack', 'azure_openai', 'google_workspace'
    encrypted_credentials = Column(Text, nullable=False)  # JSON encrypted credentials
    is_active = Column(Boolean, default=True)
    last_tested_at = Column(DateTime, nullable=True)
    test_status = Column(String, nullable=True)  # 'success', 'failed', 'pending'
    test_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="credentials")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)  # 'login', 'credential_update', 'slack_message', etc.
    resource_type = Column(String, nullable=True)  # 'credential', 'user', 'message', etc.
    resource_id = Column(String, nullable=True)
    details = Column(JSON, nullable=True)  # Additional details in JSON format
    ip_address = Column(String, nullable=True)
    status = Column(String, default="success")  # 'success', 'failed', 'error'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")


class UsageStats(Base):
    __tablename__ = "usage_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_type = Column(String, nullable=False)  # 'slack', 'azure_openai', 'google_drive'
    action_type = Column(String, nullable=False)  # 'message', 'summary', 'query', etc.
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    execution_time_ms = Column(Float, nullable=True)
    meta_info = Column(JSON, nullable=True)  # Renamed from 'metadata' to avoid SQLAlchemy reserved name
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="usage_stats")


class SlackMessage(Base):
    __tablename__ = "slack_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    slack_user_id = Column(String, nullable=False)
    slack_channel_id = Column(String, nullable=False)
    slack_message_ts = Column(String, nullable=False)  # Slack message timestamp
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0)
    response_time_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Summary(Base):
    __tablename__ = "summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    source_messages = Column(JSON, nullable=True)  # List of message IDs or content
    google_drive_file_id = Column(String, nullable=True)
    google_drive_file_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="summaries")
