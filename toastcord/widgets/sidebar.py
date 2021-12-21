from functools import lru_cache

from textual.widgets import (
    TreeClick, TreeControl, TreeNode
)

from textual.reactive import Reactive

from rich.text import Text
from rich.console import RenderableType

from toastcord import client
from toastcord.widgets.click import Click
from toastcord.api.types.guild import Guild
from toastcord.utils.panel import get_panel


class Sidebar(TreeControl):

    def __init__(self, name: str = "") -> None:
        super().__init__("👾 ToastCord", name=name, data=None)
        self.root.tree.guide_style = "black"

    has_focus: Reactive[bool] = Reactive(False)

    def render(self) -> RenderableType:
        panel = get_panel()
        panel.renderable = self._tree
        return panel

    def on_focus(self) -> None:
        self.has_focus = True

    def on_blur(self) -> None:
        self.has_focus = False

    @lru_cache(maxsize=1024 * 32)
    def render_tree_label(
        self, node: TreeNode, is_hover: bool
    ) -> RenderableType:

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label = Text(node.label) if isinstance(node.label, str) else node.label

        icon = "🧩" if isinstance(node.data, Guild) else "#"

        if is_hover:
            label.stylize("bold green")
        else:
            label.stylize("dim green")

        icon_label = Text(icon, no_wrap=True, overflow="ellipsis") + label
        icon_label.apply_meta(meta)

        return icon_label

    def render_node(self, node: TreeNode) -> RenderableType:
        return self.render_tree_label(
            node,
            node.is_cursor,
            node.id == self.hover_node,
            self.has_focus,
        )

    async def on_mount(self) -> None:
        await self.root.add("📝 Direct messages ", data="Direct messages")
        await self.root.add("📝 Guilds", data="Guilds")

        for direct_message in client.channels:
            await self.root.children[0].add(
                direct_message.recipient.username,
                data=direct_message
            )

        for guild in client.guilds:
            await self.root.children[1].add(
                str(guild.name),
                data=guild
            )

        await self.root.expand()
        await self.root.children[0].expand()
        await self.root.children[1].expand()

        self.refresh(layout=True)

    async def handle_tree_click(self, message: TreeClick) -> None:

        if isinstance(message.node.data, Guild):
            await message.node.data.load_channels()

            ids = (node.data.id for node in message.node.children)

            for channel in message.node.data.channels:
                if channel.id not in ids:
                    await message.node.add(channel.name, channel)

            if message.node.expanded is False:
                await message.node.expand()

        await self.emit(Click(self, message.node.data))
