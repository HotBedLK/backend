from fastapi import APIRouter,Depends
from supabase import Client
from typing import Annotated
from app.database.supabase import get_supabase_client
from ..schemas.loginInputSchema import LoginInputSchema
from ..services.loginService import loginService
from app.utils.rate_limiter import RateLimiter

router  = APIRouter(tags=["Auth Routes"])

@router.post("/login",description="login a user in the system")
def login(data : LoginInputSchema, 
          db: Annotated[Client, Depends(get_supabase_client)],
          _: Annotated[None, Depends(RateLimiter(limit=5, window_seconds=60, key_prefix="register"))]
          ):
    return loginService(loginData=data.model_dump(),db=db)

