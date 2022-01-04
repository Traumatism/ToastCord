from rich.panel import Panel
from rich.columns import Columns

from typing import AsyncIterable

from textual.widgets import ScrollView

from toastcord import client


class MessagesBox(ScrollView):

    async def render(self):

        if client.selected_channel is not None:
            columns = Columns(
                [panel async for panel in self.parse_messages()],
                align="left"
            )

            await self.update(columns)

        return self.layout

    # async def on_message(self, message: Message) -> None:
    #     if isinstance(message, ChannelEscape):
    #         client.selected_channel = None
    #         self.layout.reset()
    #         self.reset_check_layout()
    #         await self.render()

    async def parse_messages(self) -> AsyncIterable[Panel]:
        """ Parse the messages in the channel """
        if client.selected_guild is not None:
            return  # TODO: Guild informations

        if client.selected_channel is None:
            return  # ???

        async for message in client.selected_channel.load_messages():
            yield message.render()
