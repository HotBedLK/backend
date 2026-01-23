from supabase import Client
from postgrest.exceptions import APIError
from ..exceptions.generalUserEXceptions import SupabaseApiFailException
from typing import Optional, List, Dict, Any
import random


class Transactions:
    """
    Repository layer for interacting with the database
    """
    
    @staticmethod
    def FetchLandingDemoPostsRepoFunc(db: Client,limit: Optional[int] = 12) -> List[Dict[str, Any]]:
        """
        get demo 12 posts from database
        """
        try:
            all_property_count = db.table("Propeties").select("*",count="exact",head=True).execute()
            #check datbase all posts count and if count is lesser than our limit. we return all records. else we get random selected properties
            if all_property_count.count <= limit:
                data = db.from_("Propeties").select("id, property_type, price,location_name, Images(id, image)").execute()
                return data
            data = db.from_("Propeties").select("id, property_type, price, location_name,Images(id, image)").range(1,12).execute()
            
        except APIError as exc:
            raise SupabaseApiFailException(message=str(exc)) from exc
        except Exception as e:
            print(f"Error in FetchLandingDemoPostsRepoFunc: {e}")
            raise SupabaseApiFailException(message=str(e)) from e
