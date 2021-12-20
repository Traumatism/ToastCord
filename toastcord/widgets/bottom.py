from rich.console import RenderableType

from textual.widget import Widget

from toastcord import client
from toastcord.utils.panel import get_panel
from toastcord.widgets.click import MessageSent
from toastcord.api.types.channels import GuildChannel, MessageChannel


class Bottom(Widget):

    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name)
        self.user_input = ""

    def render(self) -> RenderableType:
        if client.selected_channel is None:
            return ""

        panel = get_panel()

        panel.border_style = "bold red"

        panel.renderable = (
            f"(null) 👉 '{self.user_input}'"
        )

        if isinstance(client.selected_channel, GuildChannel):
            panel.renderable = (
                f"(#{client.selected_channel.name}) 👉 '{self.user_input}'"
            )

        if isinstance(client.selected_channel, MessageChannel):
            panel.renderable = (
                f"({client.selected_channel.recipient}) 👉 '{self.user_input}'"
            )

        return panel

    async def on_event(self, event) -> None:
        if client.selected_channel is None:
            return

        try:
            key = event.key
        except AttributeError:
            return

        if key == "ctrl+h":
            self.user_input = self.user_input[:-1]
        elif key == "enter":
            await client.selected_channel.send_message(self.user_input)
            self.user_input = ""  # flush input
            await self.emit(MessageSent(self))
        else:
            self.user_input += key

        self.refresh(layout=True)
