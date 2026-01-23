from fastapi import APIRouter
from services.AdminService.app.main import app
from fastapi import Depends
from typing import Annotated
from supabase import Client
from app.database.supabase import get_supabase_client

router  = APIRouter(tags=["General user routes"])

#used for get single property post details required post id from the frontend
@router.get(path="/post-details/{post_id}",description="This endpoint used for fetch single post details")
def GetSinglePostController(db: Annotated[Client, Depends(get_supabase_client)],post_id:str):
    pass