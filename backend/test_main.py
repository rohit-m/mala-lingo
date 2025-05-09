import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

# Mock Supabase responses
@pytest.fixture
def mock_supabase_auth():
    with patch("main.supabase") as mock_supabase:
        # Setup auth mock
        mock_auth = MagicMock()
        mock_supabase.auth = mock_auth
        
        # Setup user response
        mock_user = MagicMock()
        mock_user.id = "user-id-123"
        mock_user.email = "test@example.com"
        
        # Setup session response
        mock_session = MagicMock()
        mock_session.access_token = "mock-access-token"
        
        # Setup auth response
        mock_auth_response = MagicMock()
        mock_auth_response.user = mock_user
        mock_auth_response.session = mock_session
        
        # Setup auth methods
        mock_auth.sign_up.return_value = mock_auth_response
        mock_auth.sign_in_with_password.return_value = mock_auth_response
        mock_auth.get_user.return_value = mock_user
        
        yield mock_supabase


@pytest.fixture
def mock_supabase_table():
    with patch("main.supabase") as mock_supabase:
        # Setup table mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        
        # Setup execute response
        mock_execute = MagicMock()
        mock_execute.data = [
            {"id": 1, "malayalam_word": "manga", "english_meaning": "mango"},
            {"id": 2, "malayalam_word": "bhakshanam", "english_meaning": "food"},
            {"id": 3, "malayalam_word": "chore", "english_meaning": "rice"},
            {"id": 4, "malayalam_word": "kadala", "english_meaning": "beans"},
            {"id": 5, "malayalam_word": "kadala", "english_meaning": "beans"},
        ]
        
        # Setup table chain
        mock_table.select.return_value.execute.return_value = mock_execute
        
        yield mock_supabase


# /api/auth/signup tests
def test_signup_success(mock_supabase_auth):
    """Test successful user signup"""
    response = client.post(
        "/api/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    
    assert response.status_code == 200
    assert "User created successfully" in response.json()["message"]
    mock_supabase_auth.auth.sign_up.assert_called_once()


def test_signup_failure(mock_supabase_auth):
    """Test failed user signup"""
    # Make the signup method raise an exception
    mock_supabase_auth.auth.sign_up.side_effect = Exception("Email already registered")
    
    response = client.post(
        "/api/auth/signup",
        json={"email": "existing@example.com", "password": "password123"}
    )
    
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


# /api/auth/login tests
def test_login_success(mock_supabase_auth):
    """Test successful user login"""
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert response.json()["access_token"] == "mock-access-token"
    mock_supabase_auth.auth.sign_in_with_password.assert_called_once()


def test_login_failure(mock_supabase_auth):
    """Test failed user login"""
    # Make the login method raise an exception
    mock_supabase_auth.auth.sign_in_with_password.side_effect = Exception("Invalid credentials")
    
    response = client.post(
        "/api/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpassword"}
    )
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


# /api/auth/user tests
def test_get_user_success(mock_supabase_auth):
    """Test successful user retrieval"""
    response = client.get("/api/auth/user?token=valid-token")
    
    assert response.status_code == 200
    assert "user" in response.json()
    mock_supabase_auth.auth.get_user.assert_called_once_with("valid-token")


# /api/word-matching tests
def test_get_word_matching_success(mock_supabase_table):
    """Test successful word matching data retrieval"""
    response = client.get("/api/word-matching")
    
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]) == 5
    mock_supabase_table.table.assert_called_once_with("word_matching")


def test_get_word_matching_few_entries(mock_supabase_table):
    """Test word matching with fewer than 5 entries"""
    # Change the data to have fewer than 5 entries
    mock_execute = mock_supabase_table.table.return_value.select.return_value.execute.return_value
    mock_execute.data = [
        {"id": 1, "malayalam_word": "ആപ്പിൾ", "english_meaning": "apple"},
        {"id": 2, "malayalam_word": "പഴം", "english_meaning": "fruit"}
    ]
    
    response = client.get("/api/word-matching")
    
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2 