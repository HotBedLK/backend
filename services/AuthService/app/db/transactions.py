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

    @staticmethod
    def get_user_for_verification_by_email(email: str, db: Client):
        try:
            response = (
                db.table("Users")
                .select("id,email,mobile_number,verification_token,verified,created_at")
                .eq("email", email)
                .execute()
            )
            if not response.data:
                return None
            return response.data[0]
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def get_user_for_verification_by_mobile(number: str, db: Client):
        try:
            response = (
                db.table("Users")
                .select("id,email,mobile_number,verification_token,verified,created_at")
                .eq("mobile_number", number)
                .execute()
            )
            if not response.data:
                return None
            return response.data[0]
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def mark_user_verified(user_id: str, db: Client, verified_time: str):
        try:
            response = (
                db.table("Users")
                .update({"verified": True, "verifired_time": verified_time})
                .eq("id", user_id)
                .execute()
            )
            return response.data
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def update_verification_token(user_id: str, token_hash: str, db: Client):
        try:
            response = (
                db.table("Users")
                .update({"verification_token": token_hash, "verified": False})
                .eq("id", user_id)
                .execute()
            )
            return response.data
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def create_otp_attempt(payload: dict, db: Client):
        try:
            response = db.table("otp_attempts").insert(payload).execute()
            return response.data
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc

    @staticmethod
    def get_latest_otp_attempt(user_id: str, db: Client):
        try:
            response = (
                db.table("otp_attempts")
                .select("id,otp_hash,sent_at,expires_at,send_count,status")
                .eq("user_id", user_id)
                .order("sent_at", desc=True)
                .limit(1)
                .execute()
            )
            if not response.data:
                return None
            return response.data[0]
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
