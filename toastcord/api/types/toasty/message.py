import os

from toastcord.utils.panel import get_panel

from dataclasses import dataclass


@dataclass
class ToastyMessage:
    """ A message from Toasty """
    content: str

    def render(self):
        """ Render message """

        title = '[bright_black][bold][green]Toasty[/green][/bold]'

        panel = get_panel()

        panel.renderable = (
            self.content + "\n" + (" " * os.get_terminal_size().columns)
        )

        panel.title = title
        panel.title_align = "left"
        panel.border_style = "red"
        panel.expand = True

        return panel
