import re

from rich.markup import escape

from dataclasses import dataclass

from typing import AsyncIterable, List, Union

from toastcord.api.types import DiscordObject
from toastcord.api.types.user import User
from toastcord.api.types.message import Message, ToastBotMessage
from toastcord.api.http import AsyncHTTPClient

PATTERN = r"(?P<date>\d{4}\-\d{2}\-\d{2})T(?P<hour>\d{2}\:\d{2}\:\d{2})"


@dataclass
class Channel(DiscordObject):
    """ A channel """
    messages: List[Union[Message, ToastBotMessage]]

    def __init__(self) -> None:
        if not issubclass(self.__class__, (GuildChannel, MessageChannel)):
            raise NotImplementedError("you cannot instantiate this class")

    def __hash__(self) -> int:
        return self.id

    async def send_message(self, message: str):
        """ Send a message to the user """
        await AsyncHTTPClient.post(
            f"/channels/{self.id}/messages", data={"content": message}
        )

    async def load_messages(self, limit: int = 100) -> AsyncIterable[Message]:
        """ Load channel messages """
        response = await AsyncHTTPClient.get(
            f"/channels/{self.id}/messages?limit={limit}"
        )

        for message in response:
            author = User(
                id=message["author"]["id"],
                username=message["author"]["username"],
                discriminator=message["author"]["discriminator"]
            )

            raw_timestamp = message["timestamp"]

            parsed_timestamp = re.search(PATTERN, raw_timestamp)

            if parsed_timestamp is None:
                continue

            yield Message(
                id=message["id"], author=author,
                content=escape(message["content"]),
                timestamp=parsed_timestamp.group("hour"),
                date=parsed_timestamp.group("date")
            )


@dataclass
class MessageChannel(Channel):
    """ A message channel """
    recipient: User


@dataclass
class GuildChannel(Channel):
    """ A guild channel """
    name: str

    allow_reading: bool = True
    allow_writing: bool = True
