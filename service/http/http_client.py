import httpx

class HTTPClientPool:
    def __init__(self, max_connections=100, max_keepalive=20, timeout=10.0):
        self.client = httpx.AsyncClient(
            limits=httpx.Limits(max_connections=max_connections, max_keepalive_connections=max_keepalive),
            timeout=timeout
        )

    async def get(self, url, **kwargs):
        response = await self.client.get(url, **kwargs)
        response.raise_for_status()
        return response

    async def post(self, url, data=None, json=None, **kwargs):
        response = await self.client.post(url, data=data, json=json, **kwargs)
        response.raise_for_status()
        return response

    async def close(self):
        await self.client.aclose()