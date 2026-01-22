from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from .api.registerAuth import router as register_router
from .api.verifyAuth import router as verify_router
from .api.resendOtpAuth import router as resend_otp_router
from fastapi.exceptions import RequestValidationError
from .exceptions.registerExceptions import RegisterException
from .api.loginAuth import router as login_router

app = FastAPI(title="Auth Service")



app.include_router(register_router)
app.include_router(verify_router)
app.include_router(resend_otp_router)
app.include_router(login_router)



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    messages = []
    for error in exc.errors():
        messages.append(error["msg"])

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "error_code": "VALIDATION_ERROR",
            "error_message": messages[0],
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
        },
    )

#services wise exception handlers
@app.exception_handler(RegisterException)
async def app_exception_handler(request: Request, exc: RegisterException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "error_message": exc.error_message,
            "status_code": exc.status_code,
        },
    )
