import toastcord

from textual.widgets import TreeClick, TreeControl, TreeNode
from textual.reactive import Reactive

from rich.text import Text
from rich.console import RenderableType

from toastcord.api.types.guild import Guild
from toastcord.api.types.channels import Channel
from toastcord.utils.messages import ChannelChanged, Click

LOGO = Text("ToastCord", style="blue")


class Sidebar(TreeControl):

    def __init__(self, name: str = "sidebar") -> None:
        super().__init__(LOGO, name=name, data=0)

        self.root.tree.guide_style = "black"

    has_focus: Reactive[bool] = Reactive(False)

    def render(self) -> RenderableType:
        return self._tree

    def on_focus(self) -> None:
        self.has_focus = True

    def on_blur(self) -> None:
        self.has_focus = False

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
        await self.root.add("Direct messages ", data=1)
        await self.root.add("Guilds", data=2)
        await self.root.add("Manage friends", data=3)

        async for direct_message in toastcord.client.channels_async():
            await self.root.children[0].add(
                direct_message.recipient.username, data=direct_message
            )

        async for guild in toastcord.client.guilds_async():
            await self.root.children[1].add(str(guild.name), data=guild)

        self.refresh(layout=True)

    async def handle_tree_click(self, message: TreeClick) -> None:

        if message.node.data in (0, 1, 2, 3):
            await message.node.toggle()
            return self.refresh()

        if isinstance(message.node.data, Guild):
            ids = {node.data.id for node in message.node.children}

            async for channel in message.node.data.load_channels():
                if channel.id not in ids:
                    await message.node.add(channel.name, channel)

            await message.node.toggle()

        if isinstance(message.node.data, Channel):
            toastcord.client.selected_channel = message.node.data
            await self.emit(ChannelChanged(self))

        await self.emit(Click(self, message.node.data))
