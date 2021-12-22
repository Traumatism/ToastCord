import os

from rich.console import RenderableType

from typing import Union

from textual.widget import Widget

from toastcord import client
from toastcord.utils.panel import get_panel
from toastcord.widgets.messages import MessageSent
from toastcord.api.types.channels import GuildChannel, MessageChannel


class Input(Widget):

    def __init__(self, name: Union[str, None] = None) -> None:
        super().__init__(name=name)

        self.user_input = ""

    def render(self) -> RenderableType:

        if client.selected_channel is None:
            return ""

        panel = get_panel()
        panel.border_style = "cyan"

        if isinstance(client.selected_channel, GuildChannel):
            panel.title = (
                "[bright_black]"
                f"# {client.selected_channel.name}"
                "[/bright_black]"
            )

        if isinstance(client.selected_channel, MessageChannel):
            panel.title = (
                "[bright_black]"
                f"@ {client.selected_channel.recipient} "
                f"({client.selected_channel.recipient.id})"
                "[/bright_black]"
            )

        panel.title_align = "left"

        panel.renderable = (
            self.user_input + (" " * os.get_terminal_size().columns)
        )

        return panel

    async def on_event(self, event) -> None:
        self.refresh()

        try:
            key = event.key
        except AttributeError:
            return

        if client.selected_channel is None:
            return

        if key == "ctrl+h":
            self.user_input = self.user_input[:-1]

        elif key == "enter":
            await client.selected_channel.send_message(self.user_input)
            self.user_input = ""  # flush input
            await self.emit(MessageSent(self))
        else:
            self.user_input += key if len(key) == 1 else ""

        self.refresh(layout=True)
