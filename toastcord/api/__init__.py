import requests

from dataclasses import dataclass
from typing import List, Dict

from toastcord.arguments import arguments


# Discord API version
API_VERSION = "v9"

API_BACKEND = (
    "https://canary.discord.com/api/%(version)s" % {"version": API_VERSION}
)


class HTTPClient:

    def __init__(self) -> None:
        self.token = arguments.token

    @property
    def headers(self) -> Dict[str, str]:
        """ Get headers """
        return {"Authorization": self.token}

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


http_client = HTTPClient()


@dataclass
class User:
    """ A Discord user """
    id: int
    username: str
    discriminator: str

    selected: bool = False

    def __eq__(self, __o: "User") -> bool:
        return self.id == __o.id

    def __str__(self) -> str:
        selection_indicator = ' > ' if self.selected is True else ''

        return f"{selection_indicator}{self.username}#{self.discriminator}"


@dataclass
class Message:
    """ A message """
    id: int
    author: User
    content: str
    timestamp: str


@dataclass
class MessageChannel:
    """ A message channel """
    id: int
    recipient: User
    messages: List[Message]

    async def load_messages(self, limit: int = 25):
        """ Load channel messages """
        response = http_client.get(
            f"/channels/{self.id}/messages?limit={limit}"
        )

        for message in response:
            author = User(
                id=message["author"]["id"],
                username=message["author"]["username"],
                discriminator=message["author"]["discriminator"]
            )

            self.messages.append(Message(
                id=message["id"], author=author,
                content=message["content"], timestamp=message["timestamp"]
            ))


class Client:
    """ A minimalist Discord API wrapper """

    def __init__(self) -> None:
        ...

    def initalize(self):
        self.user = self.__user

    @property
    def channels(self):
        """ Get all channels """
        response = http_client.get("/users/@me/channels")
        channels = []

        for channel in response:

            if len(channel["recipients"]) != 1:
                continue

            user = User(
                id=channel["recipients"][0]["id"],
                username=channel["recipients"][0]["username"],
                discriminator=channel["recipients"][0]["discriminator"]
            )

            channels.append(MessageChannel(
                id=channel["id"],
                recipient=user,
                messages=[]
            ))

        return channels

    @property
    def __user(self) -> User:
        """ Get the current user """
        response = http_client.get("/users/@me")

        return User(
            id=response["id"],
            username=response["username"],
            discriminator=response["discriminator"]
        )
