from dataclasses import dataclass

from toastcord.api.types import DiscordObject
from toastcord.api.types.user import User


@dataclass
class Message(DiscordObject):
    """ A message """
    author: User
    content: str
    timestamp: str
    date: str

    def render(self):
        """ Render the message """
