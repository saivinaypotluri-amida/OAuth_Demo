import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_database():
    """Clean up database before each test"""
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def auth_token():
    """Create user and return auth token"""
    client.post(
        "/api/auth/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        }
    )
    
    response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    return response.json()["access_token"]


def test_create_credential(auth_token):
    """Test creating a credential"""
    response = client.post(
        "/api/credentials/",
        json={
            "service_type": "slack",
            "credentials": {
                "bot_token": "xoxb-test-token",
                "signing_secret": "test-secret"
            }
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["service_type"] == "slack"
    assert data["is_active"] == True


def test_get_credentials(auth_token):
    """Test getting all credentials"""
    # Create a credential first
    client.post(
        "/api/credentials/",
        json={
            "service_type": "slack",
            "credentials": {
                "bot_token": "xoxb-test-token",
                "signing_secret": "test-secret"
            }
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.get(
        "/api/credentials/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["service_type"] == "slack"


def test_delete_credential(auth_token):
    """Test deleting a credential"""
    # Create a credential first
    client.post(
        "/api/credentials/",
        json={
            "service_type": "slack",
            "credentials": {
                "bot_token": "xoxb-test-token",
                "signing_secret": "test-secret"
            }
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    response = client.delete(
        "/api/credentials/slack",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(
        "/api/credentials/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert len(get_response.json()) == 0


def test_invalid_service_type(auth_token):
    """Test creating credential with invalid service type"""
    response = client.post(
        "/api/credentials/",
        json={
            "service_type": "invalid_service",
            "credentials": {
                "test": "data"
            }
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400


def test_unauthorized_access():
    """Test accessing credentials without authentication"""
    response = client.get("/api/credentials/")
    assert response.status_code == 401
