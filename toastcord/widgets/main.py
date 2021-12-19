from textual.app import App
from textual.widgets import ScrollView

from rich.panel import Panel

from toastcord import WELCOME_SCREEN, client

from .sidebars.channels import ChannelsSidebar
from .sidebars.guilds import GuildsSidebar
from .click import ChannelClick


class MainWindow(App):
    """ Main TUI window """

    async def on_mount(self) -> None:
        self.body = ScrollView()

        await self.view.dock(
            ScrollView(ChannelsSidebar()), ScrollView(GuildsSidebar()),
            edge="left", name="sidebar", size=30
        )

        await self.view.dock(self.body, edge="top")

    async def handle_channel_click(self, message: ChannelClick) -> None:
        if message.channel.id == 1337:
            await self.body.update(WELCOME_SCREEN)
            return

        await self.body.update("Loading messages...")

        await message.channel.load_messages()

        text = ""

        for x in message.channel.messages.__reversed__():
            style = "dim" if x.author == client.user else "bold"

            text += f"[{style}]"
            text += f'[white]{x.author}[/white]: '
            text += f"[green]{x.content}[/green]"
            text += f"[/{style}]"

            text += "\n\n"

        await self.body.update(Panel(text))
