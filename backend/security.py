from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import json
import base64
import logging
from config import settings
from database import get_db
from models import User
from schemas import TokenData

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Encryption for storing credentials
# In production, use a key management service
ENCRYPTION_KEY = base64.urlsafe_b64encode(settings.secret_key.encode().ljust(32)[:32])
cipher_suite = Fernet(ENCRYPTION_KEY)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    # Bcrypt has a 72 byte limit, truncate password bytes if necessary
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes and decode back to string
        plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password - bcrypt has a 72 byte limit"""
    # Bcrypt has a 72 byte limit, truncate password bytes if necessary
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes and decode back to string  
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> TokenData:
    """Verify JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id_str: str = payload.get("sub")
        role: str = payload.get("role")
        token_type_in_payload: str = payload.get("type")
        
        logger.debug(f"Token payload: sub={user_id_str}, role={role}, type={token_type_in_payload}")
        
        # Convert user_id from string to int (JWT standard uses string for sub)
        if user_id_str is None:
            logger.error("Token missing 'sub' field")
            raise credentials_exception
        
        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid user_id in token: {user_id_str}, error: {e}")
            raise credentials_exception
        
        if token_type_in_payload != token_type:
            logger.error(f"Token type mismatch: expected {token_type}, got {token_type_in_payload}")
            raise credentials_exception
        
        token_data = TokenData(user_id=user_id, role=role)
        return token_data
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise credentials_exception


def encrypt_credentials(credentials: dict) -> str:
    """Encrypt credentials for storage"""
    credentials_json = json.dumps(credentials)
    encrypted = cipher_suite.encrypt(credentials_json.encode())
    return encrypted.decode()


def decrypt_credentials(encrypted_credentials: str) -> dict:
    """Decrypt stored credentials"""
    decrypted = cipher_suite.decrypt(encrypted_credentials.encode())
    return json.loads(decrypted.decode())


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_data = verify_token(token)
        logger.debug(f"Token verified for user_id: {token_data.user_id}")
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise credentials_exception
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    
    if user is None:
        logger.error(f"User not found with id: {token_data.user_id}")
        raise credentials_exception
    
    if not user.is_active:
        logger.error(f"User {token_data.user_id} is not active")
        raise credentials_exception
    
    logger.debug(f"User authenticated successfully: {user.username}")
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current user and verify admin role"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
