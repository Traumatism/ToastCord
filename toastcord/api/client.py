from typing import AsyncIterable, Iterable, Optional

from toastcord.api.http import HTTPClient, AsyncHTTPClient

from toastcord.api.types import DiscordID
from toastcord.api.types.user import User
from toastcord.api.types.guild import Guild
from toastcord.api.types.channels import MessageChannel, Channel


class Client:
    """ A minimalist Discord API wrapper """

    def __init__(self, token: str) -> None:

        self.selected_channel: Optional[Channel] = None
        self.selected_guild: Optional[Guild] = None

        self.token = token

    def initalize(self):
        try:
            self.user = self.__user
        except KeyError:
            return False
        return True

    async def guilds_async(self) -> AsyncIterable[Guild]:
        """ Get all guilds asynchronously """
        response = await AsyncHTTPClient.get("/users/@me/guilds")

        for guild in response:
            yield Guild(
                id=guild["id"],
                name=guild["name"]
            )

    @property
    def guilds(self) -> Iterable[Guild]:
        """ Get all guilds """
        response = HTTPClient.get("/users/@me/guilds")

        for guild in response:
            yield Guild(id=guild["id"], name=guild["name"])

    async def channels_async(self) -> AsyncIterable[MessageChannel]:
        """ Get all channels asynchronously """
        response = await AsyncHTTPClient.get("/users/@me/channels")

        for channel in response:

            if len(channel["recipients"]) != 1:
                continue

            user = User(
                id=channel["recipients"][0]["id"],
                username=channel["recipients"][0]["username"],
                discriminator=channel["recipients"][0]["discriminator"]
            )

            last_message_id = (
                channel["last_message_id"]
                or DiscordID(0)
            )

            yield MessageChannel(
                id=channel["id"],
                recipient=user,
                messages=[],
                last_message_id=last_message_id
            )

    @property
    def channels(self) -> Iterable[MessageChannel]:
        """ Get all channels """
        response = HTTPClient.get("/users/@me/channels")

        for channel in response:

            if len(channel["recipients"]) != 1:
                continue

            user = User(
                id=channel["recipients"][0]["id"],
                username=channel["recipients"][0]["username"],
                discriminator=channel["recipients"][0]["discriminator"]
            )

            last_message_id = (
                channel["last_message_id"]
                or DiscordID(0)
            )

            yield MessageChannel(
                id=channel["id"],
                recipient=user,
                messages=[],
                last_message_id=last_message_id
            )

    @property
    def __user(self) -> User:
        """ Get the current user """
        response = HTTPClient.get("/users/@me")

        return User(
            id=response["id"],
            username=response["username"],
            discriminator=response["discriminator"]
        )
