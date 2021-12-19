import os

from rich.table import Table

from textual.app import App
from textual.widgets import ScrollView

from toastcord import WELCOME_SCREEN, client

from toastcord.utils.panel import get_panel
from toastcord.api.types.channels import GuildChannel

from .header import Header
from .click import ChannelClick, GuildClick
from .sidebars.guilds import GuildsSidebar
from .sidebars.channels import ChannelsSidebar


class MainWindow(App):
    """ Main TUI window """

    async def on_mount(self) -> None:
        panel = get_panel()
        panel.renderable = WELCOME_SCREEN
        panel.height = os.get_terminal_size().lines - 3

        self.body = ScrollView(panel)

        await self.view.dock(Header(), edge="top", size=3)

        await self.view.dock(
            ScrollView(ChannelsSidebar()), ScrollView(GuildsSidebar()),
            edge="left", name="sidebar", size=30
        )

        await self.view.dock(self.body, edge="top")

    async def handle_guild_click(self, message: GuildClick) -> None:
        if isinstance(message.guild, GuildChannel):
            return

        await message.guild.load_informations()

        table = Table.grid(padding=(0, 1), expand=True)

        table.add_column("Key", style="yellow")
        table.add_column("Value", style="red")

        table.add_row("Name", message.guild.name)
        table.add_row("Description", message.guild.description)
        table.add_row("Owner ID", str(message.guild.owner_id))
        table.add_row("Channel count", str(len(message.guild.channels)))

        panel = get_panel()
        panel.renderable = table

        await self.body.update(panel)

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

        panel = get_panel()
        panel.renderable = text

        await self.body.update(panel)
