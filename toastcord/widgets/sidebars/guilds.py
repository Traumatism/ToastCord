from functools import lru_cache

from typing import Union

from textual import events
from textual.reactive import Reactive
from textual.widgets import TreeClick, TreeControl, TreeNode, NodeID

from rich.text import Text
from rich.console import RenderableType


from ..click import ChannelClick, GuildClick

from toastcord import client
from toastcord.api.types.channels import MessageChannel, GuildChannel
from toastcord.api.types.user import User
from toastcord.api.types.guild import Guild


class GuildsSidebar(TreeControl):
    """ Sidebar for guilds """

    def __init__(self, name: str = None) -> None:

        self.home_channel = MessageChannel(
            id=1337,
            recipient=User(id=1337, username="null", discriminator=1337),
            messages=[]
        )

        super().__init__(
            "👾 Guilds",
            name=name, data=self.home_channel
        )

        self.root.tree.guide_style = "black"

    async def on_key(self, event: events.Key) -> None:
        return await super().on_key(event)

    has_focus: Reactive[bool] = Reactive(False)

    def on_focus(self) -> None:
        self.has_focus = True

    def on_blur(self) -> None:
        self.has_focus = False

    async def watch_hover_node(self, hover_node: NodeID) -> None:
        for node in self.nodes.values():
            node.tree.guide_style = "black"

        self.refresh(layout=True)

    def render_node(self, node: TreeNode[Guild]) -> RenderableType:
        return self.render_tree_label(
            node,
            node.is_cursor,
            node.id == self.hover_node,
            self.has_focus,
        )

    @lru_cache(maxsize=1024 * 32)
    def render_tree_label(
        self,
        node: TreeNode[Guild],
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
            label.stylize("bold green")
        else:
            label.stylize("dim green")

        if is_cursor and has_focus:
            label.stylize("reverse")

        icon_label = Text(icon, no_wrap=True, overflow="ellipsis") + label
        icon_label.apply_meta(meta)

        return icon_label

    async def on_mount(self, event: events.Mount) -> None:
        await self.load_guilds(self.root)

    async def load_guilds(self, node: TreeNode[Guild]):
        """ Load guilds inside the tree """
        guilds = client.guilds

        for entry in guilds:
            await node.add(str(entry.name), entry)

        node.loaded = True

        await node.expand()

        self.refresh(layout=True)

    async def handle_tree_click(
        self, message: TreeClick[Union[GuildChannel, Guild]]
    ) -> None:
        """ Handle click """

        if message.node.data.id == 1337:
            return

        if isinstance(message.node.data, Guild):

            await message.node.data.load_channels()

            ids = (node.data.id for node in message.node.children)

            for channel in message.node.data.channels:
                if channel.id not in ids:
                    await message.node.add(str(channel.name), channel)

            if message.node.expanded is False:
                await message.node.expand()

            await self.emit(GuildClick(self, message.node.data))
        else:
            await self.emit(ChannelClick(self, message.node.data))
