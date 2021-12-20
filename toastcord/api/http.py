import requests

from typing import Dict

from ..arguments import arguments

# Discord API version
API_VERSION = "v9"

API_BACKEND = (
    "https://canary.discord.com/api/%(version)s" % {"version": API_VERSION}
)

TOKEN = arguments.token


class AsyncHTTPClient:
    """ A minimalistic asynchronous HTTP client for the Discord API """
    ...


class HTTPClient:
    """ A minimalistic HTTP client for the Discord API """

    def __init__(self) -> None:
        pass

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
        return {"Authorization": TOKEN}

    def get(self, endpoint: str, params: Dict = {}) -> Dict:
        """ Get data from the API """
        return requests.get(
            API_BACKEND + endpoint,  headers=self.headers, params=params
        ).json()

    def post(
        self, endpoint: str, data: Dict = {}, params: Dict = {}
    ) -> Dict:
        """ Post data to the API """
        return requests.post(
            API_BACKEND + endpoint,
            headers=self.headers, data=data,  params=params
        ).json()
