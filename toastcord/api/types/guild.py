from dataclasses import dataclass
from typing import List, Union

from toastcord.api.types.user import User

from .channels import GuildChannel
from ..http import HTTPClient

http_client = HTTPClient()


@dataclass
class Guild:
    """ A guild """
    id: int
    name: str
    channels: List[GuildChannel]

    description: str = ""
    owner_id: int = 0
    count: int = 0

    async def load_informations(self):
        response = http_client.get(f"/guilds/{self.id}")

        self.description = response["description"]
        self.owner_id = response["owner_id"]

    async def load_channels(self):
        """ Load channels """
        self.channels = []
        response = http_client.get(f"/guilds/{self.id}/channels")

        for channel in response:
            if channel["type"] != 0:
                continue

            self.channels.append(GuildChannel(
                id=channel["id"], name=channel["name"],
                messages=[],
            ))

    def __hash__(self) -> int:
        return int(self.id)
