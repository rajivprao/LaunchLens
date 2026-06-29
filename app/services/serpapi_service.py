import httpx

from app.config.settings import Secrets

# Demand Data

class SerpApiService:

    BASE_URL = "https://serpapi.com/search.json"

    def __init__(self):

        secrets = Secrets()
        self.api_key = secrets.SERP_API_KEY

    # Generic Request Method
    async def _request(self, params: dict):

        params["api_key"] = self.api_key
        async with httpx.AsyncClient(timeout=60) as client:

            response = await client.get(self.BASE_URL,params=params)
            response.raise_for_status()
            return response.json()

    async def google_search(self,query: str,tbs:str=""):

        query_dict = {"engine": "google","q": query,"gl":"in","hl":"en"}
        if tbs != "":
            query_dict["tbs"] = tbs

        return await self._request(query_dict)

    async def google_trends(self,query: str):
        return await self._request({"engine": "google_trends","q": query,"geo":"IN","hl":"en",
                                    "date": "today 12-m","data_type": "TIMESERIES"})
    
    async def google_news(self,query: str):
        return await self._request({"engine": "google_news","q": query,"gl":"in","hl":"en"})

    async def google_shopping(self,query: str):
        return await self._request({"engine": "google_shopping","q": query,"gl":"in","hl":"en"})
    
            


