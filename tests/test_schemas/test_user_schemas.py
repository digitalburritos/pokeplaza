import uuid
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest

# Fixtures for common test data
@pytest.fixture
def user_base_data():
    return {
        "nickname": "john_doe_123",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "AUTHENTICATED",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe"
    }

@pytest.fixture
def user_create_data(user_base_data):
    return {**user_base_data, "password": "SecurePassword123!"}

@pytest.fixture
def user_update_data():
    return {
        "email": "john.doe.new@example.com",
        "nickname": "j_doe",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I specialize in backend development with Python and Node.js.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg"
    }

@pytest.fixture
def user_response_data(user_base_data):
    return {
        "id": uuid.uuid4(),
        "nickname": user_base_data["nickname"],
        "first_name": user_base_data["first_name"],
        "last_name": user_base_data["last_name"],
        "role": user_base_data["role"],
        "email": user_base_data["email"],
        # "last_login_at": datetime.now(),
        # "created_at": datetime.now(),
        # "updated_at": datetime.now(),
        "links": []
    }

@pytest.fixture
def login_request_data():
    return {"email": "john_doe_123@emai.com", "password": "SecurePassword123!"}

# Tests for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data["nickname"]
    assert user.password == user_create_data["password"]

# Tests for UserUpdate
def test_user_update_valid(user_update_data):
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.first_name == user_update_data["first_name"]

# Tests for UserResponse
def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    # assert user.last_login_at == user_response_data["last_login_at"]

# Tests for LoginRequest
def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

def test_user_update_valid(user_update_data, user_base_data):
    """Test case to verify the correct update of a user's information."""
    # First, create a user (this is a mock or can be an actual API request in a real test)
    user = UserBase(**user_base_data)
    
    # Now update the user's data
    user_update = UserUpdate(**user_update_data)
    user.nickname = user_update.nickname
    user.email = user_update.email
    user.first_name = user_update.first_name
    user.last_name = user_update.last_name
    user.bio = user_update.bio
    user.profile_picture_url = user_update.profile_picture_url
    
    # Assert the fields are updated correctly
    assert user.nickname == user_update.nickname
    assert user.email == user_update.email
    assert user.first_name == user_update.first_name
    assert user.last_name == user_update.last_name
    assert user.bio == user_update.bio
    assert user.profile_picture_url == user_update.profile_picture_url

def test_user_update_invalid_email(user_update_data, user_base_data):
    """Test case to verify that an invalid email format triggers validation error."""
    # Create user with valid data
    user = UserBase(**user_base_data)
    
    # Set invalid email format
    user_update_data["email"] = "invalid-email-format"
    
    # Check if validation error is raised when attempting to update the email
    with pytest.raises(ValidationError):
        UserUpdate(**user_update_data)

def test_user_update_missing_required_fields(user_update_data, user_base_data):
    """Test case to verify that missing required fields cause validation errors."""
    # Create user with valid data
    user = UserBase(**user_base_data)
    
    # Remove required fields for testing
    user_update_data.pop("email")
    
    # Attempting to update without email should raise a validation error
    with pytest.raises(ValidationError):
        UserUpdate(**user_update_data)

def test_user_update_partial(user_update_data, user_base_data):
    """Test case to verify partial updates where some fields are unchanged."""
    # Create user with initial data
    user = UserBase(**user_base_data)
    
    # Simulate updating only part of the user data
    partial_update_data = {key: value for key, value in user_update_data.items() if key in ['email', 'bio']}
    user_update = UserUpdate(**partial_update_data)
    
    user.email = user_update.email
    user.bio = user_update.bio
    
    # Assert that the fields are updated, and others remain the same
    assert user.email == user_update.email
    assert user.bio == user_update.bio
    assert user.nickname == user_base_data["nickname"]  # Check if nickname is unaffected

def test_user_update_invalid_url(user_update_data, user_base_data):
    """Test case to verify that an invalid URL format triggers a validation error."""
    # Create user with valid data
    user = UserBase(**user_base_data)
    
    # Set invalid URL format in the update data
    user_update_data["profile_picture_url"] = "ftp://invalid-url.com/profile.jpg"
    
    # Attempting to update the user with an invalid URL should raise a validation error
    with pytest.raises(ValidationError):
        UserUpdate(**user_update_data)

