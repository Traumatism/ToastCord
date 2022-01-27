from rich.console import RenderableType

from typing import AsyncIterable

from textual.widgets import ScrollView

from toastcord import client
from toastcord.utils.panel import get_panel


class MessagesBox(ScrollView):
    """ Box where the messages will be displayed """

    async def render(self):
        if client.selected_channel is not None:

            msgs = []

            async for message in self.parse_messages():
                msgs.append(message)

            panel = get_panel()
            panel.renderable = "\n\n".join(msgs)
            panel.highlight = False

            await self.update(panel)

        return self.layout

    async def parse_messages(self) -> AsyncIterable[RenderableType]:
        """ Parse the messages in the channel """

        if client.selected_channel is None:
            return

        async for message in client.selected_channel.load_messages():
            yield message.render()
