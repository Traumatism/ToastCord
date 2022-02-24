import os
import toastcord

from rich.text import Text
from rich.markup import escape
from rich.console import RenderableType

from typing import Optional

from textual.app import App
from textual.keys import Keys
from textual.reactive import Reactive
from textual.events import Key, Focus, Blur

from textual.widget import Widget
from textual.widgets import Footer as _Footer

from textual.widgets import (
    ScrollView, TreeClick, TreeControl, TreeNode
)

from toastcord import WELCOME_SCREEN
from toastcord.utils.messages import ChannelChanged, Click, MessageReload
from toastcord.api.types.channels import GuildChannel, MessageChannel
from toastcord.api.types.guild import Guild
from toastcord.api.types.channels import Channel
from toastcord.utils.panel import get_panel


class MainWindow(App):
    """ Main window """

    async def on_mount(self) -> None:

        self.body = MessagesBox(WELCOME_SCREEN)
        self.sidebar = ScrollView(Sidebar())

        self.input = Input()
        self.footer = Footer()

        await self.view.dock(self.footer, edge="bottom")

        await self.view.dock(self.input, edge="bottom", size=10)

        await self.view.dock(
            self.sidebar, edge="left", size=30, name="sidebar"
        )

        await self.view.dock(self.body, edge="top")

        await self.bind("r", "update_messages", "Update messages")
        await self.bind("s", "toggle_sidebar", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")

    async def on_message(self, message) -> None:
        """ Handle messages """
        if isinstance(message, MessageReload):
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

    async def handle_click(self, message: Click) -> None:
        """ Handle a click event """
        if not isinstance(message.target, (Channel, Guild)):
            return

        await self.body.render()


class Input(Widget):
    """ Input widget """

    def __init__(self, name: Optional[str] = None) -> None:
        super().__init__(name=name)

        self.user_input = ""

    has_focus: Reactive[bool] = Reactive(False)

    def render(self) -> RenderableType:
        """ Render the widget """

        if toastcord.client.selected_channel is None:
            return ""

        base = f"[{'white' if self.has_focus else 'bright_black'}]"
        base += ("─" * os.get_terminal_size().columns) + "\n"
        base += f"[/{'white' if self.has_focus else 'bright_black'}]"

        if isinstance(toastcord.client.selected_channel, GuildChannel):
            base += (
                "(Channel) [bright_black]("
                f"[white]{toastcord.client.selected_channel.name}[/white]"
                ")[/bright_black] > "
            )

        elif isinstance(toastcord.client.selected_channel, MessageChannel):
            base += (
                "(DM) [bright_black]("
                f"[white]{toastcord.client.selected_channel.recipient}[/white]"
                ")[/bright_black] > "
            )

        else:
            base += (
                "[bright_black]([red]"
                "Please select a channel[/red]"
                ")[/bright_black]"
            )

        return base + escape(self.user_input)

    async def on_event(self, event) -> None:
        """ Handle events """

        self.refresh()

        if isinstance(event, (Blur, Focus)):
            self.has_focus = not self.has_focus
            return self.refresh()

        if (
            not isinstance(event, Key)
            or toastcord.client.selected_channel is None
        ):
            return

        key = event.key

        if (
            key not in {"ctrl+h", "enter"}
            and key in list(map(lambda x: x.value, list(iter(Keys))))
        ):
            return

        elif key == "ctrl+h":
            self.user_input = self.user_input[:-1]

        elif key == "enter":
            await toastcord.client.selected_channel.send_message(
                self.user_input
            )

            self.user_input = ""

            await self.emit(MessageReload(self))
        else:
            self.user_input += key

        return self.refresh()


class Footer(_Footer):
    """ Override the footer to show the key bindings """

    def make_key_text(self) -> Text:
        """ Create text containing all the keys """

        text = Text(
            style="white",
            no_wrap=True, overflow="ellipsis",
            justify="left", end=""
        )

        for binding in self.app.bindings.shown_keys:
            key_text = Text.assemble(
                f" ({Text(binding.description, style='white on cyan')}) ",
                meta={
                    "@click": f"app.press('{binding.key}')", "key": binding.key
                },
            )
            text.append_text(key_text)

        return text


class MessagesBox(ScrollView):
    """ Box where the messages will be displayed """

    async def render(self):
        """ Render the message box """

        selected_channel = toastcord.client.selected_channel

        if selected_channel is None:
            return

        messages = []

        async for message in selected_channel.load_messages():
            messages.append(message.render())

        panel = get_panel()

        panel.border_style = "white"
        panel.renderable = "\n\n".join(messages)

        await self.update(panel)

        return self.layout


LOGO = Text("ToastCord", style="blue")


class Sidebar(TreeControl):

    def __init__(self, name: str = "sidebar") -> None:
        super().__init__(LOGO, name=name, data=0)

        self.root.tree.guide_style = "black"

    def render_tree_label(
        self, node: TreeNode, is_cursor: bool, expanded: bool
    ) -> RenderableType:

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label = (
            Text(node.label, style="blue")
            if isinstance(node.label, str) else node.label
        )

        if is_cursor:
            label.stylize("bold cyan")

        if expanded:
            label.stylize("bold")

        icon = ("#" if isinstance(node.data, Channel) else "@") + " "

        icon_label = (
            Text(icon, no_wrap=True, overflow="ellipsis", style="bright_black")
            + label
        )

        icon_label.apply_meta(meta)

        return icon_label

    def render_node(self, node: TreeNode) -> RenderableType:
        return self.render_tree_label(
            node, node.id == self.hover_node, node.expanded
        )

    async def on_mount(self) -> None:
        """ Mount the sidebar """

        await self.root.add("Direct messages ", data=1)
        await self.root.add("Guilds", data=2)

        _channels = {}

        async for direct_message in toastcord.client.channels_async():
            _channels[direct_message.last_message_id] = direct_message

        _ids = map(str, reversed(sorted(map(int, _channels.keys()))))

        for x in _ids:
            if x == "0":
                continue

            direct_message = _channels[x]

            await self.root.children[0].add(
                direct_message.recipient.username, data=direct_message
            )

        async for guild in toastcord.client.guilds_async():
            await self.root.children[1].add(str(guild.name), data=guild)

        self.refresh(layout=True)

    async def handle_tree_click(self, message: TreeClick) -> None:
        """ Handle a click event """

        if message.node.data in (0, 1, 2, 3):
            await message.node.toggle()
            return self.refresh()

        if isinstance(message.node.data, Guild):
            toastcord.client.selected_guild = message.node.data

            ids = {node.data.id for node in message.node.children}

            async for channel in message.node.data.load_channels():
                if channel.id not in ids:
                    await message.node.add(channel.name, channel)

            await message.node.toggle()

        if isinstance(message.node.data, Channel):
            toastcord.client.selected_channel = message.node.data
            await self.emit(ChannelChanged(self))

        await self.emit(Click(self, message.node.data))
