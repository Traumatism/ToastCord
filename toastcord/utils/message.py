import os

from toastcord import client
from toastcord.utils.panel import get_panel
from toastcord.api.types.message import Message, ToastBotMessage


def render_toastbot_message(message: ToastBotMessage):
    """ Render message from ToastBot """

    panel = get_panel()

    panel.renderable = (
        message.content + "\n" + (" " * os.get_terminal_size().columns)
    )

    panel.title = "[red bold]👾 ToastBot [/red bold]"
    panel.title_align = "left"
    panel.border_style = "yellow"
    panel.expand = True

    return panel


def render_message(message: Message):
    """ Render message """

    title = (
        f"[bright_black][bold][green]{message.author.username}[/green][/bold]"
        f" [italic]on {message.date} at {message.timestamp}"
        "[/italic][/bright_black]"
    )

    panel = get_panel()

    panel.renderable = (
        message.content + "\n" + (" " * os.get_terminal_size().columns)
    )

    panel.title = title
    panel.title_align = "left"
    panel.border_style = "blue" if message.author == client.user else "cyan"
    panel.expand = True

    return panel
