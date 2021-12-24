from rich.columns import Columns
from rich.panel import Panel

from typing import AsyncIterable

from textual.widgets import ScrollView

from toastcord import client

from toastcord.utils.message import render_message


class MessagesBox(ScrollView):

    async def render(self):
        if client.selected_channel is not None:
            columns = [panel async for panel in self.parse_messages()]
            await self.update(Columns(columns, align="left"))

        return self.layout

    async def parse_messages(self) -> AsyncIterable[Panel]:
        """ Parse the messages in the channel """
        if client.selected_channel is None:
            return

        async for message in client.selected_channel.load_messages():
            yield render_message(message)
