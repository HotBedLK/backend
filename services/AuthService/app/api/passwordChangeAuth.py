from fastapi import APIRouter,Depends
from supabase import Client
from typing import Annotated
from app.database.supabase import get_supabase_client
from ..schemas.changePasswordSchema import ChangePasswordInputSchema
from app.utils.rate_limiter import RateLimiter
from ..services.channgePasswordService import changePasswordService

router  = APIRouter(tags=["Auth Routes"])


@router.post('/change_password',description="change user password after the email verification")
async def change_password(data : ChangePasswordInputSchema, 
          db: Annotated[Client, Depends(get_supabase_client)],
          _: Annotated[None, Depends(RateLimiter(limit=5, window_seconds=60, key_prefix="change_password"))]
          ):
    return changePasswordService(changePasswordData=data.model_dump(),db=db)