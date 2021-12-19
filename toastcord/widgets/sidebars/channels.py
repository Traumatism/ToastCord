from functools import lru_cache

from textual import events
from textual.widgets import (
    TreeClick, TreeControl, TreeNode, NodeID
)

from textual.reactive import Reactive

from rich.text import Text
from rich.console import RenderableType

from toastcord import client

from ..click import ChannelClick

from toastcord.api.types.channels import MessageChannel
from toastcord.api.types.user import User


class ChannelsSidebar(TreeControl):
    """ Sidebar for channels """

    def __init__(self, name: str = None) -> None:

        self.home_channel = MessageChannel(
            id=1337,
            recipient=User(id=1337, username="test", discriminator=1337),
            messages=[]
        )

        super().__init__(
            "👾 Direct messages", name=name, data=self.home_channel
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
