from dataclasses import dataclass
from typing import List, Tuple

from .channels import GuildChannel
from ..http import AsyncHTTPClient

http_client = AsyncHTTPClient()


@dataclass
class Guild:
    """ A guild """

    id: int
    name: str
    channels: List[GuildChannel]

    description: str = ""

    owner_id: int = -1
    count: int = -1

    async def load_informations(self) -> Tuple[str, str, int, int]:
        """ Load guild informations """
        response = await http_client.get(f"/guilds/{self.id}")

        self.description = response["description"]
        self.owner_id = response["owner_id"]

        return self.description, self.owner_id, self.count, self.count

    async def load_channels(self) -> List[GuildChannel]:
        """ Load channels """
        self.channels = []
        response = await http_client.get(f"/guilds/{self.id}/channels")

        for channel in response:
            if channel["type"] != 0:
                continue

            self.channels.append(GuildChannel(
                id=channel["id"], name=channel["name"],
                messages=[],
            ))

        return self.channels

    def __hash__(self) -> int:
        return int(self.id)
