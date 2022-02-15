import toastcord
import requests
import aiohttp

from typing import Dict, Optional


FULL_URL = (
    toastcord.API_BACKEND
    if not toastcord.API_BACKEND.endswith('/') else toastcord.API_BACKEND[:-1]
)

HEADERS = {
    "Authorization": toastcord.TOKEN,
    "User-Agent": toastcord.USER_AGENT,
}

API_BACKEND = (
    "%(url)s/%(version)s" % {"version": toastcord.API_VERSION, "url": FULL_URL}
)


class HTTPClient:
    """ A minimalistic HTTP client for the Discord API """

    @staticmethod
    def get(endpoint: str, params: Optional[Dict] = None) -> Dict:
        """ Get data from the API """

        if params is None:
            params = {}

        response = requests.get(
            API_BACKEND + endpoint, headers=HEADERS, params=params
        )

        return response.json()

    @staticmethod
    def post(
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict:
        """ Post data to the API """

        response = requests.post(
            API_BACKEND + endpoint, headers=HEADERS, data=data, params=params
        )

        return response.json()


class AsyncHTTPClient:
    """ Same as HTTPClient, but asynchronous """

    @staticmethod
    async def get(endpoint: str, params: Optional[Dict] = None) -> Dict:
        """ Get data from the API """

        async with aiohttp.ClientSession() as session:
            async with session.get(
                API_BACKEND + endpoint,
                headers=HEADERS,
                params=params
            ) as response:
                return await response.json()

    @staticmethod
    async def post(
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict:
        """ Post data to the API """

        async with aiohttp.ClientSession() as session:

            async with session.post(
                API_BACKEND + endpoint,
                headers=HEADERS,
                params=params,
                data=data
            ) as response:
                return await response.json()
