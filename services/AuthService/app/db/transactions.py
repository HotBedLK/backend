from supabase import Client
from postgrest.exceptions import APIError
from ..exceptions.registerExceptions import SupabaseApiFailException

class Transactions:
    #check user existance via email address
    @staticmethod
    def check_user_by_email(email, db: Client):
        try:
            user = db.table("Users").select("email").eq('email',email).execute()
            if len(user.data) == 0:
                return False
            return True
        except APIError:
            raise SupabaseApiFailException(message="something happened on our end!")
        

    #check user existance via email address
    @staticmethod
    def check_user_by_phonenumber(number, db: Client):
        try:
            user = db.table("Users").select("mobile_number").eq('mobile_number',number).execute()
            if len(user.data) == 0:
                return False
            return True
        except APIError:
            raise SupabaseApiFailException(message="something happened on our end!")              
        
    # check mobile number is exist or not
    @staticmethod
    def check_user_by_mobile_number(number, db: Client):
        try:
            user = db.table("Users").select("mobile_number").eq('mobile_number',number).execute()
            if len(user.data) == 0:
                return False
            return {
                'data' : user.data[0],
                'status' : True
            }
        except APIError:
            raise SupabaseApiFailException(message="something happened on our end!")