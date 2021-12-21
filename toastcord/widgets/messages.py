import rich.repr

from typing import Union

from textual.message import Message, MessageTarget

from toastcord.api.types.guild import Guild
from toastcord.api.types.channels import Channel, GuildChannel


@rich.repr.auto
class Click(Message, bubble=True):
    """ Handle click """

    def __init__(
        self, sender: MessageTarget,
        target: Union[Guild, Channel, GuildChannel]
    ) -> None:
        self.target = target
        super().__init__(sender)


@rich.repr.auto
class Key(Message, bubble=True):
    """ Handle key press """

    def __init__(self, sender: MessageTarget, target: str) -> None:
        self.target = target
        super().__init__(sender)


@rich.repr.auto
class ChannelChanged(Message, bubble=True):
    """ Handle channel changing """

    def __init__(self, sender: MessageTarget) -> None:
        super().__init__(sender)


@rich.repr.auto
class MessageSent(Message, bubble=True):
    """ Handle message sending """

    def __init__(self, sender: MessageTarget) -> None:
        super().__init__(sender)
