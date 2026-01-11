from pydantic import BaseModel, EmailStr, validator, Field,field_validator

class RegisterInputSchema(BaseModel):
    first_name: str = Field(..., min_length=1, description="First name is required")
    last_name: str = Field(..., min_length=1, description="Last name is required")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    mobile_number: str = Field(..., description="Mobile number must be 10 digits")
    email: EmailStr = Field(..., description="A valid email address is required")

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

    @field_validator("mobile_number")
    def validate_mobile_number(cls, value):
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits")
        if len(value) != 10:
            raise ValueError("Mobile number must be exactly 10 digits")
        return value
