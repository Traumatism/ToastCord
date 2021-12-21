import requests

from typing import Dict

from ..arguments import arguments

BASE = "https://%(backend)s/%(version)s"

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
        return {"Authorization": arguments.token}

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
