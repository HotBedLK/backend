from ..db.transactions import Transactions
from ..exceptions.registerExceptions import UserEmailAlreadyExistsException,UserNumberAlreadyExistsException

def registerService(registerData,db):
    """
    Docstring for registerService
    Register a user using user details and send sms otp messages to phone number
    """

    #check user existance by email address
    exist_userByEmail = Transactions.check_user_by_email(email=registerData["email"],db=db)
    if exist_userByEmail:
        raise UserEmailAlreadyExistsException(message="This email is already exists in the system. try to login with that email.")
    
    #check user existance by phone number
    exist_userByNumber = Transactions.check_user_by_phonenumber(number=registerData["mobile_number"],db=db)
    if exist_userByNumber:
        raise UserNumberAlreadyExistsException(message="This email is already exists in the system. try to login with that email")
    

    #send otp code to the user
    #TODO implement
    #save user and otp code in database
    #TODO implement
    



