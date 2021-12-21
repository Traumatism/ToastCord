from rich.columns import Columns
from rich.panel import Panel

from typing import List

from textual.app import App
from textual.widgets import ScrollView

from toastcord import (
    WELCOME_SCREEN, client
)

from toastcord.utils.message import (
    render_message, render_toastbot_message
)
from toastcord.utils.panel import get_panel

from toastcord.widgets.header import Header
from toastcord.widgets.input import Input
from toastcord.widgets.sidebar import Sidebar

from toastcord.widgets.messages import (
    ChannelChanged, Click, MessageSent
)

from toastcord.api.types.guild import Guild
from toastcord.api.types.message import ToastBotMessage
from toastcord.api.types.channels import Channel


class MainWindow(App):

    async def on_mount(self) -> None:

        self.body = ScrollView(WELCOME_SCREEN)
        self.sidebar = ScrollView(Sidebar())
        self.bottom = Input()

        self.body.name = ""
        self.sidebar.name = ""

        await self.view.dock(Header(), edge="top", size=3)

        await self.view.dock(
            self.sidebar, edge="left", name="sidebar", size=40
        )

        await self.view.dock(self.bottom, edge="bottom", size=10)

        await self.view.dock(self.body, edge="top")

        await self.bind("r", "update_messages")

    async def on_message(self, message) -> None:
        if isinstance(message, MessageSent):
            await self.update_messages()

        if isinstance(message, Click):
            await self.handle_click(message)

        if isinstance(message, ChannelChanged):
            self.bottom.refresh()

    async def action_update_messages(self) -> None:
        await self.update_messages()

    async def parse_messages(self) -> List[Panel]:

        if client.selected_channel is None:
            return []

        await client.selected_channel.load_messages()

        return [
            render_toastbot_message(message)
            if isinstance(message, ToastBotMessage)
            else render_message(message)
            for message in client.selected_channel.messages
        ]

    async def update_messages(self) -> None:
        if client.selected_channel is None:
            return

        columns = await self.parse_messages()

        await self.body.update(Columns(columns, align="left"))

    async def handle_click(self, message: Click) -> None:

        if not isinstance(message.target, (Channel, Guild)):
            return

        if isinstance(message.target, Guild):
            panel = get_panel()
            panel.renderable = "Select a channel to start chatting"

            await self.body.update(panel)

            return self.refresh()

        await self.update_messages()
