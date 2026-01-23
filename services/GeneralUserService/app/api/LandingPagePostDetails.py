from fastapi import APIRouter

"""
NOTE controller task : in this controller i fetch limited details from post that loaded in to the landing page.
not authorized user cannot see the whole details. this endpoint only returns limited setup of details only 
"""

router  = APIRouter(tags=["General user routes"])

@router.get("/landing-feed-post-details/{property_id}",description="this return landing page properties details with limited setup")
def PostDetailsController():
    pass

