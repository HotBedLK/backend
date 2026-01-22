from fastapi import APIRouter
from supabase import Client
from typing import Annotated
from fastapi import Depends
from app.database.supabase import get_supabase_client

router  = APIRouter(tags=["General user routes"])

#route for get random 12 post from the database
@router.get("/demos",description="get random 12 post from the database")
def register(db: Annotated[Client, Depends(get_supabase_client)]):
    pass