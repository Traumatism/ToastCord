import rich.repr

from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import SIMPLE

from functools import lru_cache

from textual.widgets import (
    TreeControl, TreeNode, TreeClick,
    NodeID, ScrollView
)

from textual.message import MessageTarget, Message
from textual.reactive import Reactive
from textual.widget import Widget
from textual.app import App
from textual import events

from typing import Union

from toastcord.api import MessageChannel, Client, User

WELCOME_SCREEN = """

[cyan]   ╔╦╗╔═╗╔═╗╔═╗╔╦╗[/cyan]  ┌─┐┌─┐┬─┐┌┬┐[blue bold]  #####[/blue bold] [bold white]< want some toast?[/bold white]
[cyan]    ║ ║ ║╠═╣╚═╗ ║[/cyan]   │  │ │├┬┘ ││[blue bold] ##[bold white]@[/bold white]#[bold white]@[/bold white]##[/blue bold]
[cyan]    ╩ ╚═╝╩ ╩╚═╝ ╩[/cyan]   └─┘└─┘┴└┘└┴┘[blue bold]  ## ##[/blue bold]

    Developed by toast#3108

    https://github.com/traumatism/ToastCord

    https://t.me/toastakerman
    https://github.com/traumatism
    https://twitter.com/toastakerman
"""

selected_channel: Union[MessageChannel, None] = None

client: Client = Client()


@rich.repr.auto
class ChannelClick(Message, bubble=True):
    def __init__(self, sender: MessageTarget, channel: MessageChannel) -> None:
        self.channel = channel
        super().__init__(sender)


class ChannelTree(TreeControl):

    def __init__(self, name: str = None) -> None:

        home_channel = MessageChannel(
            id=1337,
            recipient=User(id=1337, username="test", discriminator="1337"),
            messages=[]
        )

        super().__init__("📝 Direct Messages", name=name, data=home_channel)

        self.root.tree.guide_style = "black"

    has_focus: Reactive[bool] = Reactive(False)

    def on_focus(self) -> None:
        self.has_focus = True

    def on_blur(self) -> None:
        self.has_focus = False

    async def watch_hover_node(self, hover_node: NodeID) -> None:
        for node in self.nodes.values():

            node.tree.guide_style = (
                "bold not dim red" if node.id == hover_node else "black"
            )

        self.refresh(layout=True)

    def render_node(self, node: TreeNode[MessageChannel]) -> RenderableType:
        return self.render_tree_label(
            node,
            node.is_cursor,
            node.id == self.hover_node,
            self.has_focus,
        )

    @lru_cache(maxsize=1024 * 32)
    def render_tree_label(
        self,
        node: TreeNode[MessageChannel],
        is_cursor: bool,
        is_hover: bool,
        has_focus: bool,
    ) -> RenderableType:

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label = Text(node.label) if isinstance(node.label, str) else node.label
        icon = ""

        if is_hover:
            icon = "👉 "
            label.stylize("underline")
            label.stylize("bold green")
        else:
            label.stylize("dim green")

        if label.plain.startswith("."):
            label.stylize("dim")

        if is_cursor and has_focus:
            label.stylize("reverse")

        icon_label = Text(icon, no_wrap=True, overflow="ellipsis") + label
        icon_label.apply_meta(meta)
        return icon_label

    async def on_mount(self, event: events.Mount) -> None:
        await self.load_channels(self.root)

    async def load_channels(self, node: TreeNode[MessageChannel]):
        channels = client.channels

        for entry in channels:
            await node.add(str(entry.recipient), entry)

        node.loaded = True

        await node.expand()

        self.refresh(layout=True)

    async def handle_tree_click(self, message: TreeClick[MessageChannel]):
        await self.emit(ChannelClick(self, message.node.data))


class ChannelsWidget(Widget):

    async def on_load(self) -> None:
        self.set_interval(3, self.refresh)

    def render(self) -> RenderableType:
        global client

        table = Table(
            title="Channels", box=SIMPLE
        )

        table.add_column("Name", justify="left", style="bold")

        for channel in client.channels:
            table.add_row(str(channel.recipient))

        return Panel(table)


class MainWindow(App):
    """ Main TUI window """

    async def on_mount(self) -> None:
        self.body = ScrollView()

        await self.view.dock(
            ScrollView(ChannelTree()), edge="left", size=30, name="sidebar"
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

        await self.body.update(text)


if __name__ == "__main__":
    console = Console()
    client.initalize()
    MainWindow.run(console)
