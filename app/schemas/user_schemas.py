from builtins import ValueError, any, bool, str
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re

from app.utils.nickname_gen import generate_nickname

class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None:
        return url
    url_regex = r'^(https?:\/\/[^\s/$.?#].[^\s]*)$'
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format.')
    return url

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(default_factory=generate_nickname, min_length=3, example="john_doe")
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] = Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")

    @validator("nickname")
    def validate_nickname(cls, value):
        if value and not re.match(r'^[\w-]+$', value):
            raise ValueError("Nickname must consist of alphanumeric characters, underscores, or hyphens.")
        return value

    _validate_urls = validator("profile_picture_url", "linkedin_profile_url", "github_profile_url", pre=True, allow_reuse=True)(validate_url)

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str = Field(..., example="Secure*1234")

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8 or not re.search(r"[A-Z]", value) or not re.search(r"\d", value) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError(
                "Password must be at least 8 characters long and include an uppercase letter, a number, and a special character."
            )
        return value

class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")

    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update.")
        return values

class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED")
    is_professional: Optional[bool] = Field(default=False, example=True)

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="The requested resource was not found.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., example=[
        {
            "id": str(uuid.uuid4()),
            "nickname": "john_doe123",
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "bio": "Experienced developer",
            "role": "AUTHENTICATED",
            "profile_picture_url": "https://example.com/profiles/john.jpg",
            "linkedin_profile_url": "https://linkedin.com/in/johndoe",
            "github_profile_url": "https://github.com/johndoe"
        }
    ])
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)