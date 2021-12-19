from rich.panel import Panel

from textual.app import App
from textual.widgets import ScrollView

from toastcord import WELCOME_SCREEN, client
from toastcord.api.types.channels import GuildChannel

from .click import ChannelClick, GuildClick
from .sidebars.guilds import GuildsSidebar
from .sidebars.channels import ChannelsSidebar


class MainWindow(App):
    """ Main TUI window """

    async def on_mount(self) -> None:
        self.body = ScrollView(Panel(WELCOME_SCREEN))

        await self.view.dock(
            ScrollView(ChannelsSidebar()), ScrollView(GuildsSidebar()),
            edge="left", name="sidebar", size=30
        )

        await self.view.dock(self.body, edge="top")

    async def handle_guild_click(self, message: GuildClick) -> None:
        if isinstance(message.guild, GuildChannel):
            return

        await message.guild.load_informations()

        await self.body.update(Panel(
            f"""Name: {message.guild.name}
Description: {message.guild.description}
Owner ID: {message.guild.owner_id}
Channel count: {len(message.guild.channels)}"""
        ))

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
