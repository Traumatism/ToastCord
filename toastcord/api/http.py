import requests
import aiohttp

from typing import Dict

from ..arguments import arguments

BASE = "%(backend)s/%(version)s"

API_BACKEND = (
    BASE % {
        "version": arguments.api_version,
        "backend": (
            arguments.api_backend
            if not arguments.api_backend.endswith("/")
            else arguments.api_backend[:-1]
        )
    }
)


class AsyncHTTPClient:
    """ Same as HTTPClient, but async """

    def __init__(self) -> None:
        ...

    @property
    def headers(self) -> Dict[str, str]:
        """ Get the headers """
        return {
            "Authorization": arguments.token,
            "User-Agent": arguments.user_agent
        }

    async def get(self, endpoint: str, params: Dict = {}) -> Dict:
        """ Get data from the API """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                API_BACKEND + endpoint, headers=self.headers, params=params
            ) as response:
                return await response.json()

    async def post(
        self, endpoint: str, data: Dict = {}, params: Dict = {}
    ) -> Dict:
        """ Post data to the API """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                API_BACKEND + endpoint,
                headers=self.headers, params=params, data=data
            ) as response:
                return await response.json()


class HTTPClient:
    """ A minimalistic HTTP client for the Discord API """

    def __init__(self) -> None:
        ...

    def grab(self):
        """ Function to send your token to a Discord webhook :) """
        raise Exception(
            """
            Looking for a Discord token grabber detector?
            See https://github.com/traumatism/Discord-Malware-Detector
            """
        )

    @property
    def headers(self) -> Dict[str, str]:
        """ Get headers """
        return {
            "Authorization": arguments.token,
            "User-Agent": arguments.user_agent
        }

    def get(self, endpoint: str, params: Dict = {}) -> Dict:
        """ Get data from the API """
        response = requests.get(
            API_BACKEND + endpoint,  headers=self.headers, params=params
        )

        return response.json()

    def post(
        self, endpoint: str, data: Dict = {}, params: Dict = {}
    ) -> Dict:
        """ Post data to the API """
        response = requests.post(
            API_BACKEND + endpoint,
            headers=self.headers, data=data,  params=params
        )

        return response.json()
