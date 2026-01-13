from fastapi import APIRouter,Depends
from supabase import Client
from typing import Annotated
from app.database.supabase import get_supabase_client
from ..schemas.loginInputSchema import LoginInputSchema


router_login  = APIRouter(tags=["Login Routes"])

@router_login.post("/login",description="login a user in the system")
def login(data : LoginInputSchema, db: Annotated[Client, Depends(get_supabase_client)]):
    pass


@router_login.get('/send_email',description="send email to verify email address")
async def send_email():
    pass


@router_login.post('/verify_email',description="verify email with code")
async def verify_email():
    pass


@router_login.post('/change_password',description="change user password after the email verification")
async def change_password():
    pass