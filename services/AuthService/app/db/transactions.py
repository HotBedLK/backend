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
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
        

    #check user existance via email address
    @staticmethod
    def check_user_by_phonenumber(number, db: Client):
        try:
            user = db.table("Users").select("mobile_number").eq('mobile_number',number).execute()
            if len(user.data) == 0:
                return False
            return True
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def create_user(payload: dict, db: Client):
        try:
            response = db.table("Users").insert(payload).execute()
            return response.data
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
