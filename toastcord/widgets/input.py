import os
import toastcord

from rich.markup import escape
from rich.console import RenderableType

from typing import Union

from textual.keys import Keys
from textual.widget import Widget
from textual.events import Key

from toastcord.utils.panel import get_panel
from toastcord.utils.messages import MessageReload
from toastcord.api.types.channels import GuildChannel, MessageChannel


class UserInput:

    def __init__(self) -> None:
        self.__user_input = ""
        self.cursor_pos = 0
        self.max = 500

    def user_input(self, cursor=True) -> str:
        """ Get the user input """
        # escaped = escape(self.__user_input)

        # if cursor is False:
        #     return escaped

        # if len(escaped) == self.cursor_pos:
        #     escaped += "[black on white] [/black on white]"

        # elif self.cursor_pos < len(escaped):
        #     escaped = (
        #         escaped[:self.cursor_pos]
        #         + "[black on white]"
        #         + escaped[self.cursor_pos:self.cursor_pos+1]
        #         + "[/black on white]"
        #         + escaped[self.cursor_pos+1:]
        #     )

        return escape(self.__user_input)

    def flush(self) -> None:
        """ Flush the user input """
        self.__user_input = ""

    def move_left(self) -> None:
        """ Move the cursor left """
        self.cursor_pos -= 1 if self.cursor_pos > 0 else 0

    def move_right(self) -> None:
        """ Move the cursor right """
        self.cursor_pos += 1 if self.cursor_pos < len(self.__user_input) else 0

    def add_chr(self, v: str) -> None:
        """ Add a character to the user input """
        if len(self.__user_input) >= self.max:
            return

        self.cursor_pos += len(v)

        self.__user_input = (
            self.__user_input[:self.cursor_pos - 1]
            + v
            + self.__user_input[self.cursor_pos + 1:]
        )

    def remove_chr(self, x=1) -> None:
        """ Remove a character from the user input """
        self.cursor_pos -= x if self.cursor_pos > 0 else 0

        self.__user_input = (
            self.__user_input[:self.cursor_pos]
            + self.__user_input[self.cursor_pos + x:]
        )

    def remove_word(self, x=1) -> None:
        """ Remove a word from the user input """
        self.__user_input = " ".join(self.__user_input.split(" ")[:-x])


class Input(Widget):

    def __init__(self, name: Union[str, None] = None) -> None:
        super().__init__(name=name)

        self.panel_colors = ("bright_black", "white")
        self.panel_color = 0

        self.user_input: UserInput = UserInput()

    def render(self) -> RenderableType:

        if toastcord.client.selected_channel is None:
            return ""

        panel = get_panel()
        panel.highlight = False
        panel.border_style = self.panel_colors[self.panel_color]

        if isinstance(toastcord.client.selected_channel, GuildChannel):
            panel.title = (
                "[bright_black]"
                f"# {toastcord.client.selected_channel.name}"
                "[/bright_black]"
            )

        if isinstance(toastcord.client.selected_channel, MessageChannel):
            panel.title = (
                "[cyan]"
                f"@ {toastcord.client.selected_channel.recipient} "
                "[/cyan]"
            )

        panel.title_align = "left"

        panel.renderable = (
            self.user_input.user_input()
            + (" " * os.get_terminal_size().columns)
        )

        return panel

    async def on_event(self, event) -> None:
        self.refresh()

        if not isinstance(event, Key):
            return

        key = event.key

        if toastcord.client.selected_channel is None:
            return

        VALID_KEYS = {
            "left", "right",
            "ctrl+w", "ctrl+h",
            "enter"
        }

        ALL_KEYS = list(map(lambda x: x.value, list(iter(Keys))))

        # for _key in ALL_KEYS:
        #     if (
        #         key == _key
        #         and key not in VALID_KEYS
        #     ):
        #         return

        if key not in VALID_KEYS and key in ALL_KEYS:
            return

        if key == "left":
            self.user_input.move_left()

        elif key == "right":
            self.user_input.move_right()

        elif key == "ctrl+w":
            self.user_input.remove_word()

        elif key == "ctrl+h":
            self.user_input.remove_chr()

        elif key == "enter":
            await toastcord.client.selected_channel.send_message(
                self.user_input.user_input(cursor=False)
            )

            self.user_input.flush()

            await self.emit(MessageReload(self))

        else:
            self.user_input.add_chr(key)

        self.refresh()
        self.refresh(layout=True)
