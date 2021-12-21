import requests
import aiohttp

from typing import Dict

from ..arguments import arguments

BASE = "%(backend)s/%(version)s"

HEADERS = {
    "Authorization": arguments.token,
    "User-Agent": arguments.user_agent
}

full_url = (
    arguments.api_backend
    if not arguments.api_backend.endswith('/') else arguments.api_backend[:-1]
)

API_BACKEND = BASE % {"version": arguments.api_version, "backend": full_url}


class HTTPClient:
    """ A minimalistic HTTP client for the Discord API """

    @staticmethod
    def get(endpoint: str, params: Dict = {}) -> Dict:
        """ Get data from the API """
        response = requests.get(
            API_BACKEND + endpoint,  headers=HEADERS, params=params
        )

        return response.json()

    @staticmethod
    def post(endpoint: str, data: Dict = {}, params: Dict = {}) -> Dict:
        """ Post data to the API """
        response = requests.post(
            API_BACKEND + endpoint, headers=HEADERS, data=data,  params=params
        )

        return response.json()


class AsyncHTTPClient:
    """ Same as HTTPClient, but asynchronous """

    @staticmethod
    async def get(endpoint: str, params: Dict = {}) -> Dict:
        """ Get data from the API """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                API_BACKEND + endpoint, headers=HEADERS, params=params
            ) as response:
                return await response.json()

    @staticmethod
    async def post(
        endpoint: str, data: Dict = {}, params: Dict = {}
    ) -> Dict:
        """ Post data to the API """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                API_BACKEND + endpoint,
                headers=HEADERS, params=params, data=data
            ) as response:
                return await response.json()
