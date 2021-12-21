from functools import lru_cache

from textual.widgets import (
    TreeClick, TreeControl, TreeNode
)

from textual.reactive import Reactive

from rich.text import Text
from rich.console import RenderableType

from toastcord import client

from toastcord.widgets.messages import (
    ChannelChanged, Click
)

from toastcord.api.types import (
    Guild, Channel
)

LOGO = Text("ToastCord", style="blue")


class Sidebar(TreeControl):

    def __init__(self, name: str = "") -> None:
        super().__init__(LOGO, name=name, data=0)

        self.root.tree.guide_style = "black"

    has_focus: Reactive[bool] = Reactive(False)

    def render(self) -> RenderableType:
        return self._tree

    def on_focus(self) -> None:
        self.has_focus = True

    def on_blur(self) -> None:
        self.has_focus = False

    @lru_cache(maxsize=1024 * 32)
    def render_tree_label(
        self, node: TreeNode, is_hover: bool,
        is_cursor: bool, has_focus: bool, expanded: bool
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

        icon = "# " if isinstance(node.data, Channel) else "@ "

        if is_cursor:
            label.stylize("bold cyan")

        if expanded:
            label.stylize("bold")

        icon_label = (
            Text(icon, no_wrap=True, overflow="ellipsis", style="bright_black")
            + label
        )

        icon_label.apply_meta(meta)

        return icon_label

    def render_node(self, node: TreeNode) -> RenderableType:
        return self.render_tree_label(
            node,
            node.is_cursor,
            node.id == self.hover_node,
            self.has_focus,
            node.expanded
        )

    async def on_mount(self) -> None:
        await self.root.add("Direct messages ", data=1)
        await self.root.add("Guilds", data=2)
        await self.root.add("Manage friends", data=3)

        channels = await client.channels_async()

        for direct_message in channels:
            await self.root.children[0].add(
                direct_message.recipient.username, data=direct_message
            )

        for guild in client.guilds:
            await self.root.children[1].add(str(guild.name), data=guild)

        self.refresh(layout=True)

    async def handle_tree_click(self, message: TreeClick) -> None:

        if message.node.data in (0, 1, 2, 3):
            await message.node.toggle()
            return self.refresh()

        if isinstance(message.node.data, Guild):
            await message.node.data.load_channels()

            ids = (node.data.id for node in message.node.children)

            for channel in message.node.data.channels:
                if channel.id not in ids:
                    await message.node.add(channel.name, channel)

            await message.node.toggle()

        if isinstance(message.node.data, Channel):
            client.selected_channel = message.node.data
            await self.emit(ChannelChanged(self))

        await self.emit(Click(self, message.node.data))
