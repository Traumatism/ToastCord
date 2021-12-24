import os
import toastcord

from rich.console import RenderableType

from typing import Union

from textual.widget import Widget

from toastcord.utils.panel import get_panel
from toastcord.utils.messages import MessageSent
from toastcord.api.types.channels import GuildChannel, MessageChannel


class UserInput:

    def __init__(self) -> None:
        self.__user_input = ""
        self.cursor_pos = 0
        self.max = 500

    def __str__(self) -> str:
        return self.__user_input

    @property
    def prompt(self) -> str:
        return (
            str(self)
            + " [red]<[/red] [bright_black]("
            f"{len(self.__user_input)}/{self.max}"
            ")[/bright_black]"
        )

    def flush(self) -> None:
        """ Flush the user input """
        self.__user_input = ""

    def add_chr(self, v: str) -> None:
        """ Add a character to the user input """
        if len(self.__user_input) >= self.max:
            return

        self.cursor_pos += len(v)
        self.__user_input += v

    def remove_chr(self, x=1) -> None:
        """ Remove a character from the user input """
        self.cursor_pos -= x
        self.__user_input = self.__user_input[:-x]

    def remove_word(self, x=1) -> None:
        """ Remove a word from the user input """
        self.__user_input = " ".join(self.__user_input.split(" ")[:-x])


class Input(Widget):

    def __init__(self, name: Union[str, None] = None) -> None:
        super().__init__(name=name)

        self.user_input: UserInput = UserInput()

    def render(self) -> RenderableType:
        if toastcord.client.selected_channel is None:
            return ""

        panel = get_panel()
        panel.border_style = "#a84599"

        if isinstance(toastcord.client.selected_channel, GuildChannel):
            panel.title = (
                "[bright_black]"
                f"# {toastcord.client.selected_channel.name}"
                "[/bright_black]"
            )

        if isinstance(toastcord.client.selected_channel, MessageChannel):
            panel.title = (
                "[bright_black]"
                f"@ {toastcord.client.selected_channel.recipient} "
                f"({toastcord.client.selected_channel.recipient.id})"
                "[/bright_black]"
            )

        panel.title_align = "left"

        panel.renderable = (
            self.user_input.prompt + (" " * os.get_terminal_size().columns)
        )

        return panel

    async def on_event(self, event) -> None:
        self.refresh()

        try:
            key = event.key
        except AttributeError:
            return

        if toastcord.client.selected_channel is None:
            return

        if key == "ctrl+w":
            self.user_input.remove_word()

        elif key == "ctrl+h":
            self.user_input.remove_chr()

        elif key == "enter":
            await toastcord.client.selected_channel.send_message(
                str(self.user_input)
            )

            self.user_input.flush()

            await self.emit(MessageSent(self))
        else:
            self.user_input.add_chr(key)

        self.refresh(layout=True)
