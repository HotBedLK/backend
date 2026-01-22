from pydantic import BaseModel, Field, field_validator


class ChangePasswordInputSchema(BaseModel):
    mobile_number: str = Field(
        description="Mobile number used for registration (10 digits starting with 0)",
        examples=["0767722791"],
    )
    password: str = Field(
        description="Password must be at least 8 characters",
        examples=["Lakshan5656#$"],
    )

    @field_validator("mobile_number")
    def validate_mobile_number(cls, value):
        if value is None:
            return value
        if not value.isdigit():
            raise ValueError("Mobile number must contain only digits")
        if len(value) != 10 or not value.startswith("0"):
            raise ValueError("Mobile number must be 10 digits starting with 0")
        return value

    @field_validator("password")
    def require_email_or_mobile(self, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value
