import httpx

from app.config.settings import Secrets


class OxylabsService:

    BASE_URL = "https://realtime.oxylabs.io/v1/queries"
    
    ZSCALER_PROXY = "http://127.0.0.1:9000" 


    def __init__(self):
        secrets = Secrets()
        self.username = secrets.OXYLABS_API_UN
        self.password = secrets.OXYLABS_API_PW

    async def _request(self, payload: dict ):

        async with httpx.AsyncClient(timeout=60, proxy=self.ZSCALER_PROXY,verify=False) as client:

            response = await client.post(
                self.BASE_URL,
                json=payload,
                auth=(self.username,self.password)
            )

            response.raise_for_status()

            return response.json()
        
    async def amazon_search(self,keyword: str):

        payload = {"source": "amazon_search","domain":"in", "query": keyword, 
                "geo_location": "560001","parse": "true"}
        
        return await self._request(payload)

    async def amazon_product(self,asin: str):

        payload = {"source": "amazon_product","query": asin}

        return await self._request(payload)

    async def amazon_reviews(self,asin: str):

        payload = {"source": "amazon_reviews","query": asin}

        return await self._request(payload)

    async def amazon_pricing(self,asin: str):

        payload = {"source": "amazon_product","query": asin}

        return await self._request(payload)

    async def amazon_bestsellers(self,category: str):

        payload = {"source": "amazon_bestsellers","query": category}

        return await self._request(payload)                                