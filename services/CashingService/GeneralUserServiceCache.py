from redis import Redis
from functools import lru_cache
from decouple import config
from services.GeneralUserService.app.schemas.LandingDemoPostsResponse import LandingPageRedisPayload
import json
from typing import Final
from app.utils.rate_limiter import get_redis_client

@lru_cache(maxsize=1)
def GetGeneralUserRedisClient()->Redis:
    return Redis(
        host=config("REDIS_HOST", default="redis_database"),
        port=config("REDIS_PORT", default=6379, cast=int),
        password=config("REDIS_PASSWORD", default=None),
        db=1,
        decode_responses=True,
    )

class GeneralUserCacheStorage:

    LANDING_PAGE_DEMO_KEY:Final[str] = "landing:properties"
    LANDING_PAGE_DEMO_TTL :Final[int] =  600

    @staticmethod
    def SetLandingPageDemos(payload:LandingPageRedisPayload)->bool:
        """store lading page demo post array in to the redis database-1 redis database-1 beongs only to general user service only!!!"""
        try:
            row_payload = payload.model_dump(exclude_none=True,mode="json")
            r:Redis = GetGeneralUserRedisClient()
            r.setex(GeneralUserCacheStorage.LANDING_PAGE_DEMO_KEY,GeneralUserCacheStorage.LANDING_PAGE_DEMO_TTL,json.dumps(row_payload))
            return True
        except Exception as e:
            print("something happend on StoreLandingPageDemos function",e)
            return False
        
    @staticmethod
    def GetLandingPageDemos():
        """Get stored landing page demo posts from redis database-1"""
        try:
            r:Redis = GetGeneralUserRedisClient()
            cached = r.get(GeneralUserCacheStorage.LANDING_PAGE_DEMO_KEY)
            if not cached:
                return None
            data = json.loads(cached)
            return LandingPageRedisPayload.model_validate(data)
        except Exception as e:
            print("something happend on GetLandingPageDemos function",e)



        


