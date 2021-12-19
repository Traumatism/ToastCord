from dataclasses import dataclass
from typing import List

from .user import User
from .message import Message
from ..http import HTTPClient

http_client = HTTPClient()


@dataclass
class Channel:
    """ A channel """
    id: int
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


@dataclass
class MessageChannel(Channel):
    """ A message channel """
    recipient: User


@dataclass
class GuildChannel(Channel):
    """ A guild channel """
    name: str

    def __hash__(self) -> int:
        return int(self.id)
