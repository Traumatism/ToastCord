import requests
import aiohttp

from typing import Dict

import toastcord


HEADERS = {
    "Authorization": toastcord.TOKEN,
    "User-Agent": toastcord.USER_AGENT
}

full_url = (
    toastcord.API_BACKEND
    if not toastcord.API_BACKEND.endswith('/') else toastcord.API_BACKEND[:-1]
)

API_BACKEND = (
    "%(backend)s/%(version)s"
    % {"version": toastcord.API_VERSION, "backend": full_url}
)


class HTTPClient:
    """ A minimalistic HTTP client for the Discord API """

    @staticmethod
    def get(endpoint: str, params: Dict = {}) -> Dict:
        """ Get data from the API """
        response = requests.get(
            API_BACKEND + endpoint, headers=HEADERS, params=params
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
                API_BACKEND + endpoint,
                headers=HEADERS,
                params=params
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
                headers=HEADERS,
                params=params,
                data=data
            ) as response:
                return await response.json()
