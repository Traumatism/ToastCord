import os

from textual import events
from textual.app import App
from textual.widgets import ScrollView

from toastcord import WELCOME_SCREEN, client

from toastcord.utils.panel import get_panel
from toastcord.api.types.channels import Channel

from .header import Header
from .sidebar import Sidebar


class MainWindow(App):
    """ Main TUI window """

    async def on_mount(self) -> None:
        panel = get_panel()
        panel.renderable = WELCOME_SCREEN
        panel.height = os.get_terminal_size().lines - 3

        self.body = ScrollView(panel)

        panel = get_panel()
        panel.renderable = "> "
        panel.height = 5

        self.search = ScrollView(panel)

        await self.view.dock(Header(), edge="top", size=3)

        await self.view.dock(
            ScrollView(Sidebar()),
            edge="left", name="sidebar", size=30
        )

        await self.view.dock(self.body, edge="top")
        await self.view.dock(self.search, edge="top", size=10)

    async def on_key(self, event: events.Key) -> None:
        await self.search.update(event.key)

    async def handle_click(self, message):

        if isinstance(message.target, Channel):
            await self.body.update("Loading messages...")

            await message.target.load_messages()

            text = ""

            for _message in message.target.messages:
                style = "dim" if _message.author == client.user else "bold"

                text += f"[{style}]"
                text += f'[white]{_message.author}[/white]: '
                text += f"[green]{_message.content}[/green]"
                text += f"[/{style}]"

                text += "\n\n"

            panel = get_panel()
            panel.renderable = text
            panel.height = os.get_terminal_size().lines - 3

            return await self.body.update(panel)
