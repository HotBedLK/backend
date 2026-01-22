from fastapi import HTTPException

class GeneralUserExceptions(Exception):
    def __init__(
        self,
        error_code: str,
        error_message: str,
        status_code: int = 400,
    ):
        self.error_code = error_code
        self.error_message = error_message
        self.status_code = status_code


class SupabaseApiFailException(GeneralUserExceptions):
    def __init__(self, message: str):
        super().__init__(
            error_code="INTERNAL_SERVER_ERROR",
            error_message=message,
            status_code=500,
        )



