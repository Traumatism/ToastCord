import rich.repr

from typing import Union
from textual.message import Message, MessageTarget

from ..api.types.guild import Guild
from ..api.types.channels import Channel, GuildChannel


@rich.repr.auto
class ChannelClick(Message, bubble=True):
    """ Handle clicks on channels """

    def __init__(self, sender: MessageTarget, channel: Channel) -> None:
        self.channel = channel
        super().__init__(sender)


@rich.repr.auto
class GuildClick(Message, bubble=True):
    """ Handle clicks on guilds """

    def __init__(
        self, sender: MessageTarget, guild: Union[Guild, GuildChannel]
    ) -> None:
        self.guild = guild
        super().__init__(sender)
