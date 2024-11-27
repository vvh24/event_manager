from builtins import str
import pytest
from pydantic import ValidationError
from datetime import datetime
from uuid import uuid4
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest

# Fixtures for test data
@pytest.fixture
def user_base_data():
    return {
        "email": "john.doe@example.com",
        "nickname": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "Experienced developer."
    }

@pytest.fixture
def user_create_data():
    return {
        "email": "john.doe@example.com",
        "nickname": "john_doe",
        "password": "Secure*1234",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "Experienced developer."
    }

@pytest.fixture
def user_update_data():
    return {
        "email": "john.doe.updated@example.com",
        "nickname": "john_doe_updated",
        "first_name": "John Updated",
        "last_name": "Doe Updated",
        "bio": "Updated bio for the user."
    }

# Tests for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate - Password Validation
@pytest.mark.parametrize("password", ["Secure*1234", "Test@4567", "P@ssw0rd1!"])
def test_password_validation_valid(password, user_create_data):
    user_create_data["password"] = password
    user = UserCreate(**user_create_data)
    assert user.password == password

@pytest.mark.parametrize("password", ["short", "nouppercase1!", "NoNumber!", "NoSpecialChar123"])
def test_password_validation_invalid(password, user_create_data):
    user_create_data["password"] = password
    with pytest.raises(ValidationError):
        UserCreate(**user_create_data)

# Tests for UserUpdate - Profile Field Validations
@pytest.mark.parametrize("update_data", [
    {"bio": "Updated bio content."},
    {"profile_picture_url": "https://example.com/new_profile.jpg"},
    {"linkedin_profile_url": "https://linkedin.com/in/updated_profile"},
    {"github_profile_url": "https://github.com/updated_user"},
    {
        "bio": "Updated bio content.",
        "profile_picture_url": "https://example.com/new_profile.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/updated_profile"
    }
])
def test_user_update_valid_fields(update_data, user_update_data):
    user_update_data.update(update_data)
    user_update = UserUpdate(**user_update_data)
    for key, value in update_data.items():
        assert getattr(user_update, key) == value

@pytest.mark.parametrize("update_data", [
    {"profile_picture_url": "invalid_url"},
    {"linkedin_profile_url": "ftp://invalid.com/profile"},
    {"github_profile_url": "http//missing-colon.com"},
])
def test_user_update_invalid_fields(update_data, user_update_data):
    user_update_data.update(update_data)
    with pytest.raises(ValidationError):
        UserUpdate(**user_update_data)

# Test UserUpdate - No Fields Provided
def test_user_update_no_fields():
    with pytest.raises(ValidationError):
        UserUpdate()

# Tests for UserResponse
def test_user_response_valid(user_base_data):
    user_response_data = {
        **user_base_data,
        "id": uuid4(),
        "role": "AUTHENTICATED",
        "is_professional": True,
    }
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    assert user.role == user_response_data["role"]

# Tests for LoginRequest
def test_login_request_valid():
    login_request_data = {"email": "john.doe@example.com", "password": "Secure*1234"}
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]
