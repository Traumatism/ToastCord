from rich.panel import Panel
from rich.columns import Columns

from typing import AsyncIterable
from textual.widgets import ScrollView

from toastcord import client
from toastcord.utils.message import render_message
from toastcord.api.types.toasty.message import ToastyMessage


class MessagesBox(ScrollView):

    async def render(self):

        if client.selected_channel is not None:

            columns = Columns(
                [panel async for panel in self.parse_messages()],
                align="left"
            )

            await self.update(columns)

        return self.layout

    async def parse_messages(self) -> AsyncIterable[Panel]:
        """ Parse the messages in the channel """
        if client.selected_channel is None:
            return

        async for message in client.selected_channel.load_messages():
            if isinstance(message, ToastyMessage):
                yield message.render()
                continue

            yield render_message(message)
