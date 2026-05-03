from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=100)
    kata_sandi: str = Field(..., min_length=1, max_length=128)

    model_config = ConfigDict(
        json_schema_extra={"example": {"email": "admin@example.com", "kata_sandi": "password123"}}
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={"example": {"access_token": "jwt-token", "token_type": "bearer"}}
    )


class TokenPayload(BaseModel):
    sub: str
    type: str = "access"
