from dataclasses import dataclass
from typing import AsyncIterable

from toastcord.api.types import DiscordObject
from toastcord.api.types.channels import GuildChannel
from toastcord.api.http import AsyncHTTPClient


@dataclass
class Guild(DiscordObject):
    """ A guild """

    name: str
    description: str = ""

    owner_id: int = -1
    count: int = -1

    async def load_informations(self):
        """ Load guild informations """
        response = await AsyncHTTPClient.get(f"/guilds/{self.id}")

        self.description = response["description"]
        self.owner_id = response["owner_id"]

    async def load_channels(self) -> AsyncIterable[GuildChannel]:
        """ Load channels """
        response = await AsyncHTTPClient.get(f"/guilds/{self.id}/channels")

        for channel in response:
            if channel["type"] != 0:
                continue

            yield GuildChannel(
                id=channel["id"], name=channel["name"], messages=[],
            )
