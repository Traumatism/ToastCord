from typing import Union

from textual.message import Message, MessageTarget

from toastcord.api.types.guild import Guild
from toastcord.api.types.toasty.message import ToastyMessage
from toastcord.api.types.channels import Channel, GuildChannel, MessageChannel


class ToastyMessage(Message, bubble=True):
    """ Handle messages from Toasty """

    def __init__(self, sender: MessageTarget, message: ToastyMessage) -> None:
        self.message = message
        super().__init__(sender)


class Click(Message, bubble=True):
    """ Handle click """

    def __init__(
        self, sender: MessageTarget,
        target: Union[Guild, Channel, GuildChannel, MessageChannel]
    ) -> None:
        self.target = target
        super().__init__(sender)


class Key(Message, bubble=True):
    """ Handle key press """

    def __init__(self, sender: MessageTarget, target: str) -> None:
        self.target = target
        super().__init__(sender)


class ChannelChanged(Message, bubble=True):
    """ Handle channel changing """

    def __init__(self, sender: MessageTarget) -> None:
        super().__init__(sender)


class MessageReload(Message, bubble=True):
    """ Handle message reload """

    def __init__(self, sender: MessageTarget) -> None:
        super().__init__(sender)
