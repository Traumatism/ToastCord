from textual.widgets import ScrollView
from textual.app import App

from rich.panel import Panel

from toastcord import WELCOME_SCREEN, client

from .sidebars.channels import ChannelsSidebar
from .sidebars.guilds import GuildsSidebar
from .click import ChannelClick


class MainWindow(App):
    """ Main TUI window """

    async def on_mount(self) -> None:
        self.body = ScrollView(Panel(WELCOME_SCREEN))

        await self.view.dock(
            ScrollView(ChannelsSidebar()), ScrollView(GuildsSidebar()),
            edge="left", name="sidebar", size=30
        )

        await self.view.dock(self.body, edge="top")

    async def handle_channel_click(self, message: ChannelClick) -> None:

        await self.body.update("Loading messages...")

        await message.channel.load_messages()

        text = ""

        for _message in message.channel.messages:
            style = "dim" if _message.author == client.user else "bold"

            text += f"[{style}]"
            text += f'[white]{_message.author}[/white]: '
            text += f"[green]{_message.content}[/green]"
            text += f"[/{style}]"

            text += "\n\n"

        await self.body.update(Panel(text))
