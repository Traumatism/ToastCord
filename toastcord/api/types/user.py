from dataclasses import dataclass
from toastcord.api.types import DiscordObject


@dataclass
class User(DiscordObject):
    """ A Discord user """
    username: str
    discriminator: int

    def __str__(self) -> str:
        """ Returns the full username of the user """
        return f"{self.username}#{self.discriminator}"
