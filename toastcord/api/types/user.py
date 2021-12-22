from dataclasses import dataclass
from toastcord.api.types import DiscordObject


@dataclass
class User(DiscordObject):
    """ A Discord user """
    username: str
    discriminator: int

    def __str__(self) -> str:
        return f"{self.username}#{self.discriminator}"
