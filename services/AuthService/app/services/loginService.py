from ..db.transactions import Transactions
from ..exceptions.registerExceptions import credencialsNotMatchedException
from app.services.jwt import decodePasword, encodeToken
from fastapi.responses import JSONResponse


def loginService(loginData, db):
    # check the mobile number is exist or not
    user_exists = Transactions.check_user_by_mobile_number(number=loginData["mobile_number"],db=db)
    if user_exists == False:
        raise credencialsNotMatchedException("credencials not matched. please check and try again.")
    
    # if number is exist, validate the db password with plain password
    is_password_valid = decodePasword(plain_password=loginData["password"], hashed_password=user_exists['data']['password'])
    if not is_password_valid:
        raise credencialsNotMatchedException("credencials not matched. please check and try again.")

    # issue the JWT token
    token = encodeToken(email=user_exists['data']['email'], role=user_exists['data']['role'])
    return JSONResponse(status_code=200, content={
        "status" : "success",
        'data' : token
    })