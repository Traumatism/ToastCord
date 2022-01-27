import re

from dataclasses import dataclass


class DiscordID(int):
    """ A Discord unique ID """
    def __init__(self, value: int) -> None:
        if not re.match(r"^(\d{18}|0)$", str(value)):
            raise ValueError(f"{value} is not a valid Discord ID")

        self.value = value

    def __call__(self, *args, **kwds):
        return self.value


@dataclass
class DiscordObject:
    """ A Discord object """
    id: DiscordID

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, self.__class__) and self.id == __o.id
