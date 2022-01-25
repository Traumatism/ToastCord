from rich.console import RenderableType

from typing import AsyncIterable
from textual.widgets import ScrollView

from toastcord import client


class MessagesBox(ScrollView):
    async def render(self):

        if client.selected_channel is not None:

            msgs = []

            async for message in self.parse_messages():
                msgs.append(message)

            await self.update("\n\n".join(msgs))

        return self.layout

    async def parse_messages(self) -> AsyncIterable[RenderableType]:
        """ Parse the messages in the channel """

        if client.selected_channel is None:
            return

        async for message in client.selected_channel.load_messages():
            yield message.render()
