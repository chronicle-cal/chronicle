from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UpdateEmailRequest(BaseModel):
    new_email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UpdatePasswordRequest(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class UpdateNameRequest(BaseModel):
    name: str = Field(min_length=2, max_length=64)
    password: str = Field(min_length=8, max_length=128)


class DeleteAccountRequest(BaseModel):
    confirm: str
