import rich.repr

from typing import Union
from textual.message import Message, MessageTarget

from ..api.types.guild import Guild
from ..api.types.channels import Channel, GuildChannel


@rich.repr.auto
class Click(Message, bubble=True):
    """ Handle click """

    def __init__(
        self, sender: MessageTarget,
        target: Union[Guild, Channel, GuildChannel]
    ) -> None:
        self.target = target
        super().__init__(sender)
