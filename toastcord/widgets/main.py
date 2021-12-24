from textual.app import App
from textual.widgets import ScrollView

from toastcord import WELCOME_SCREEN
from toastcord.api.types.toasty.message import ToastyMessage
from toastcord.utils.panel import get_panel

from toastcord.widgets.input import Input
from toastcord.widgets.footer import Footer
from toastcord.widgets.sidebar import Sidebar
from toastcord.widgets.messagesbox import MessagesBox

from toastcord.utils.messages import (
    ChannelChanged, Click, MessageSent
)

from toastcord.api.types.guild import Guild
from toastcord.api.types.channels import Channel


class MainWindow(App):

    async def on_mount(self) -> None:

        # body, the messages contents will be displayed here
        self.body = MessagesBox(WELCOME_SCREEN)

        # sidebar, channels, guilds and friends will be displayed here
        self.sidebar = ScrollView(Sidebar())

        # Box where the user can type
        self.input = Input()

        self.footer = Footer()

        await self.view.dock(self.footer, edge="bottom")

        await self.view.dock(
            self.sidebar, edge="left", size=30, name="sidebar"
        )

        await self.view.dock(self.input, edge="bottom", size=10)
        await self.view.dock(self.body, edge="top")

        await self.bind("r", "update_messages", "Refresh messages")
        await self.bind("s", "toggle_sidebar", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")

    async def on_message(self, message) -> None:
        """ Handle messages """
        if isinstance(message, MessageSent):
            await self.body.render()

        if isinstance(message, Click):
            await self.handle_click(message)

        if isinstance(message, ChannelChanged):
            self.input.refresh()

    async def action_toggle_sidebar(self) -> None:
        """ Toggle the sidebar """
        await self.view.action_toggle("sidebar")

    async def action_update_messages(self) -> None:
        """ Update the messages in the chat window """
        await self.body.render()

    async def handle_toasty_message(self, message: ToastyMessage) -> None:
        """ Handle messages from Toasty """

    async def handle_click(self, message: Click) -> None:
        """ Handle a click event """
        if not isinstance(message.target, (Channel, Guild)):
            return

        if isinstance(message.target, Guild):
            panel = get_panel()
            panel.renderable = "Select a channel to start chatting"

            await self.body.update(panel)

            return self.refresh()

        await self.body.render()
