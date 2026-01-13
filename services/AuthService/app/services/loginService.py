from ..db.transactions import Transactions
from ..exceptions.registerExceptions import credencialsNotMatchedException

def loginService(loginData:dict,db):
    # check the mobile number is exist or not
    user_exists = Transactions.check_user_by_mobile_number(number=loginData["mobile_number"],db=db)
    if not user_exists:
        raise credencialsNotMatchedException("credencials not matched. please check and try again.")
    
    # check the password is correct or not
    
    # issue the JWT token
    pass