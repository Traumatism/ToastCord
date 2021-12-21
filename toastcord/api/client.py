from typing import Iterable, Union

from .http import HTTPClient

from .types.user import User
from .types.guild import Guild
from .types.channels import MessageChannel, Channel


class Client:
    """ A minimalist Discord API wrapper """

    def __init__(self) -> None:
        self.selected_channel: Union[Channel, None] = None

    def initalize(self):
        try:
            self.user = self.__user
        except KeyError:
            return False
        return True

    @property
    def guilds(self) -> Iterable[Guild]:
        """ Get all guilds """
        response = HTTPClient.get("/users/@me/guilds")

        for guild in response:
            yield Guild(
                id=guild["id"],
                name=guild["name"],
                channels=[]
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

            yield MessageChannel(
                id=channel["id"],
                recipient=user,
                messages=[]
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
