import toastcord

from rich.markup import escape

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

    @property
    def _content(self) -> str:
        """ Get the escaped content of the message """
        return escape(self.content)

    def render(self):
        """ Render the message """

        user_color = "blue" if self.author == toastcord.client.user else "cyan"

        message = (
            f"[{user_color} underline]"
            f"{self.author.username}"
            f"[/{user_color} underline] "
            "[bright_black italic]"
            f"({self.date} at {self.timestamp})"
            "[/bright_black italic]"
            f"\n{self.content}\n"
        )

        return message
