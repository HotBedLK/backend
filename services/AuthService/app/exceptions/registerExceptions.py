from fastapi import HTTPException

class RegisterException(Exception):
    def __init__(
        self,
        error_code: str,
        error_message: str,
        status_code: int = 400,
    ):
        self.error_code = error_code
        self.error_message = error_message
        self.status_code = status_code



class SupabaseApiFailException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="INTERNAL_SERVER_ERROR",
            error_message=message,
            status_code=500,
        )


class UserEmailAlreadyExistsException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="DUPLICATE_USER_CREATION",
            error_message=message,
            status_code=401,
        )


class UserNumberAlreadyExistsException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="DUPLICATE_USER_CREATION",
            error_message=message,
            status_code=401,
        )

class credencialsNotMatchedException(RegisterException):
    def __init__(self, message: str):
        super().__init__(
            error_code="CREDENCIALS_NOT_MATCHED",
            error_message=message,
            status_code=401,
        )