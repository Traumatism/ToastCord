from rich.columns import Columns

from textual import events
from textual.app import App
from textual.widgets import ScrollView

from toastcord import WELCOME_SCREEN, client
from toastcord.widgets.click import Click, Key, MessageSent
from toastcord.widgets.header import Header
from toastcord.widgets.bottom import Bottom
from toastcord.widgets.sidebar import Sidebar
from toastcord.api.types.channels import Channel
from toastcord.utils.message import render_message


class MainWindow(App):
    """ Main TUI window """

    async def on_mount(self) -> None:

        self.body = ScrollView(WELCOME_SCREEN, name="body")
        self.sidebar = ScrollView(Sidebar(), name="sidebar")

        await self.view.dock(Header(), edge="top", size=3)

        await self.view.dock(
            self.sidebar, edge="left", name="sidebar", size=40
        )

        await self.view.dock(Bottom(), edge="bottom", size=10)

        await self.view.dock(self.body, edge="top")

        await self.bind("r", "update_messages")

    async def on_message(self, message) -> None:
        if isinstance(message, MessageSent):
            await self.update_messages()

        if isinstance(message, Click):
            await self.handle_click(message)

    async def on_key(self, event: events.Key) -> None:
        await self.emit(Key(self, event.key))

    async def action_update_messages(self) -> None:
        await self.update_messages()

    async def update_messages(self) -> None:
        if client.selected_channel is None:
            return

        await client.selected_channel.load_messages()

        columns = (
            render_message(message)
            for message in client.selected_channel.messages
        )

        await self.body.update(Columns(columns, align="left"))

    async def handle_click(self, message):

        if not isinstance(message.target, Channel):
            return

        client.selected_channel = message.target

        await self.update_messages()
