import toastcord
import os

from dataclasses import dataclass

from toastcord.utils.panel import get_panel
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

        title = (
            f"[bright_black][bold][green]{self.author.username}[/green][/bold]"
            f" [italic]on {self.date} at {self.timestamp}"
            "[/italic][/bright_black]"
        )

        panel = get_panel()

        panel.renderable = (
            self.content + "\n" + (" " * os.get_terminal_size().columns)
        )

        panel.border_style = (
            "blue" if self.author == toastcord.client.user else "cyan"
        )

        panel.title = title
        panel.highlight = False
        panel.title_align = "left"

        return panel
